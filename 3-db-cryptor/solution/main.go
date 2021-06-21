package main

import (
	"bufio"
	"encoding/binary"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"math/rand"
	"net/http"
	"os"
	"strings"

	"solution/cipher"
)

var globalPassword string
var ctxState int

func main() {
	filename := os.Args[1]
	fileData := readBinaryFile(filename)

	magic := unpack32(fileData[0:4])
	ver := unpack32(fileData[4:8])
	timestamp := int64(unpack64(fileData[8:16]))
	yearDay := unpack64(fileData[16:24])
	entryCnt := int(unpack64(fileData[24:32]))
	encSize := unpack64(fileData[32:40])

	encrytedData := fileData[40 : encSize+40]

	fmt.Printf("Magic: %08x\nVer: %08x\nTimestamp: %016x\nYearDay: %d\nEntryCnt: %d\n",
		magic, ver, timestamp, yearDay, entryCnt)

	passwordHash := fileData[encSize+40:]
	password := unHashPassword(passwordHash)
	cipherKey := genCipherKey(password)

	decData := decryptData(encrytedData, string(cipherKey))
	globalPassword = getDayPassword(int(yearDay))
	fmt.Println("globalPassword = ", globalPassword)
	rand.Seed(timestamp)

	entryOffset := 0

	for i := 0; i < entryCnt; i++ {
		entrySize := int(unpack64(decData[entryOffset : entryOffset+8]))
		key := genEntryCipherKey()
		currentEntry := decData[entryOffset+8 : entryOffset+entrySize]
		entryOffset += (8 + entrySize)

		tmpDec := decryptData(currentEntry, string(key))
		fmt.Println("tmpDec =", string(tmpDec))
	}
}

func genCipherKey(password string) []byte {
	key := make([]byte, 16)

	for i := 0; i < len(password); i++ {
		key[i] = byte(password[i])
	}

	if len(password) != 16 {
		for i := len(password); i < 16; i++ {
			key[i] = byte(i)
		}
	}
	return key
}

func unHashPassword(passwordHash []byte) string {
	var out []byte

	table := [][]byte{
		[]byte{89, 145, 13, 127, 86, 225, 206, 138, 83, 195, 20, 237, 119, 56, 73, 28},
		[]byte{106, 108, 228, 9, 184, 175, 221, 231, 210, 185, 147, 217, 142, 131, 153, 12},
		[]byte{172, 251, 41, 162, 36, 213, 24, 16, 49, 76, 194, 2, 34, 160, 181, 232},
		[]byte{158, 254, 125, 26, 151, 218, 38, 207, 188, 157, 224, 139, 183, 208, 146, 241},
		[]byte{67, 178, 130, 68, 114, 50, 44, 71, 100, 222, 205, 77, 10, 191, 18, 252},
		[]byte{198, 30, 45, 4, 148, 226, 120, 215, 187, 78, 163, 204, 244, 171, 80, 59},
		[]byte{236, 84, 190, 82, 250, 105, 63, 75, 69, 55, 109, 22, 243, 42, 19, 201},
		[]byte{155, 229, 117, 212, 43, 81, 209, 102, 103, 126, 99, 230, 70, 92, 143, 156},
		[]byte{235, 247, 31, 255, 180, 64, 112, 0, 32, 154, 164, 96, 242, 136, 152, 122},
		[]byte{29, 182, 58, 170, 253, 118, 240, 95, 101, 169, 74, 123, 35, 79, 166, 97},
		[]byte{202, 54, 150, 90, 25, 219, 140, 3, 116, 177, 40, 159, 61, 7, 27, 110},
		[]byte{165, 161, 203, 91, 113, 39, 220, 135, 174, 176, 211, 93, 52, 66, 51, 48},
		[]byte{227, 72, 133, 233, 98, 21, 238, 5, 46, 23, 137, 200, 189, 234, 192, 149},
		[]byte{33, 111, 214, 62, 121, 186, 11, 85, 8, 94, 1, 197, 248, 107, 193, 53},
		[]byte{239, 246, 57, 128, 167, 65, 134, 141, 223, 132, 245, 249, 216, 15, 104, 60},
		[]byte{144, 173, 196, 115, 88, 37, 47, 179, 199, 87, 124, 14, 168, 6, 129, 17},
	}

	for i := 0; i < len(passwordHash); i++ {
		for r := 0; r < 16; r++ {
			for c := 0; c < 16; c++ {
				if passwordHash[i] == table[r][c] {
					//fmt.Println("r, c =", r, c)
					out = append(out, byte(r*16+c))
				}
			}
		}
	}

	return string(out)
}

func readBinaryFile(filename string) []byte {
	fd, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}

	defer fd.Close()
	reader := bufio.NewReader(fd)

	fileSize := getFileSize(fd)

	if fileSize <= 0 {
		log.Fatal("fileSize errr")
	}

	data := make([]byte, fileSize)

	for {
		_, err := reader.Read(data)

		if err != nil {
			if err != io.EOF {
				fmt.Println("err in read")
			}
			break
		}
	}
	return data
}

func getFileSize(fd *os.File) int64 {
	fi, err := fd.Stat()

	if err != nil {
		fmt.Println("[-] Can't get file size!")
		log.Fatal(err)
	}
	return fi.Size()
}

func unpack32(data []byte) uint32 {
	if len(data) > 4 {
		fmt.Println("[-] Error size!")
		log.Fatal("unpack32 error")
	}
	return binary.BigEndian.Uint32(data)
}

func unpack64(data []byte) uint64 {
	if len(data) > 8 {
		fmt.Println("[-] Error size!")
		log.Fatal("unpack64 error")
	}
	return binary.BigEndian.Uint64(data)
}

func decryptData(data []byte, key string) []byte {
	var part []byte
	var inpData []byte

	if len(data)%16 != 0 {
		inpData = make([]byte, len(data)+(16-(len(data)%16)))
	} else {
		inpData = make([]byte, len(data))
	}

	copy(inpData, data)

	for len(inpData)%16 != 0 {
		inpData = append(inpData, 0)
	}

	outData := make([]byte, len(inpData))

	for i := 0; i < len(inpData); i += 16 {
		part = inpData[i : i+16]

		enc := cipher.NewCipher([]byte(key))
		enc.Decrypt(outData[i:i+16], part)
	}

	return outData
}

func getRandomByte() byte {
	return byte(rand.Intn(0xff))
}

func genEntryCipherKey() []byte {
	ctxState++
	key := make([]byte, 16)

	for i := 0; i < 16; i++ {
		key[i] = getRandomByte() % globalPassword[ctxState%len(globalPassword)]
	}
	return key
}

func getDayPassword(day int) string {
	passwords := getUrlData("https://pastebin.com/raw/ck3TVCxe")
	passwordsList := strings.Split(passwords, "\n")
	return passwordsList[day]
}

func getUrlData(url string) string {
	resp, err := http.Get(url)

	if err != nil {
		log.Fatal("url")
	}

	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	return string(body)
}
