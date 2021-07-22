#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

#define LIST_MAX_SIZE 16
#define TITLE_MAX_SIZE 128
#define REVIEW_MAX_SIZE 256

typedef struct anime_entry {
    char* title;
    char* review;
    int score;
    struct anime_entry* next;
} AnimeEntry;

typedef struct anime_list {
    AnimeEntry* head;
    int size;
} AnimeList;

AnimeList* ListArray[LIST_MAX_SIZE];

void setup(void);
int read_int(void);
void read_buf(char*, int);

void menu(void);

int create_list(void);
int del_list(void);
int add_anime(void);
int change_review(void);
int del_anime(void);
int view_list(void);

int get_free_idx(void);
int delete_entry(AnimeEntry*, AnimeEntry*);
void free_entry(AnimeEntry*);

int main()
{
    setup();

    while (1) {
        menu();
        int option = read_int();

        if (option > 6 || option < 1)
            break;
        
        switch (option) {
            case 1:
                create_list();
                break;
            case 2:
                del_list();
                break;
            case 3:
                add_anime();
                break;
            case 4:
                change_review();
                break;
            case 5:
                del_anime();
                break;
            case 6:
                view_list();
                break;
            case 7:
            default:
                return 0;
        }
    }
    return 0;
};

void setup(void)
{
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);
};

void menu(void)
{
    puts("+-+-+ Anime List +-+-+");
    puts("1. Create list");
    puts("2. Delete list");
    puts("3. Add anime");
    puts("4. Change review");
    puts("5. Delete anime");
    puts("6. View list");
    puts("7. Exit");
    printf("> ");
};

void read_buf(char* buf, int size)
{
    int nbytes = read(0, buf, size);
    if (buf[nbytes - 1] == '\n')
        buf[nbytes - 1] = '\0';
};

int read_int(void)
{
    char buf[16];
    int nbytes = read(0, buf, 15);

    if (buf[nbytes - 1] == '\n')
        buf[nbytes - 1] = '\0';
    
    return atoi(buf); 
};

int get_free_idx(void)
{
    for (int i = 0; i < LIST_MAX_SIZE; i++) {
        if (ListArray[i] == NULL)
            return i;
    }
    return -1;
};

int create_list(void)
{
    int idx = get_free_idx();
    if (idx == -1) {
        puts("{-} No free space!");
        return 0;
    }

    ListArray[idx] = (AnimeList*) malloc(sizeof(AnimeList));
    ListArray[idx]->size = 0;
    ListArray[idx]->head = NULL;

    printf("{+} You have created list with idx %d\n", idx);
    return 1;
};

int del_list(void)
{   
    printf("{?} Enter idx: ");
    int idx = read_int();

    if (idx < 0 || idx > LIST_MAX_SIZE) {
        puts("{-} Invalid idx!");
        return 0;
    }

    if (ListArray[idx]->size == 0) {
        free(ListArray[idx]);
        ListArray[idx] = NULL;
        return 1;
    }
    
    AnimeEntry* current = ListArray[idx]->head;

    while (current != NULL) {
        AnimeEntry* p = current->next;
        free_entry(current);
        current = p;
    }

    return 1;
}

int add_anime(void)
{
    printf("{?} Enter list idx: ");
    int idx = read_int();

    if (idx < 0 || idx > LIST_MAX_SIZE) {
        puts("{-} Invalid idx!");
        return 0;
    }

    if (ListArray[idx] == NULL) {
        puts("{-} No such list!");
        return 0;
    }

    AnimeEntry* new = (AnimeEntry*) malloc(sizeof(AnimeEntry));
    new->title = (char*) malloc(TITLE_MAX_SIZE);
    new->review = (char*) malloc(REVIEW_MAX_SIZE);
    new->next = NULL;

    printf("{?} Enter anime title: ");
    read_buf(new->title, TITLE_MAX_SIZE);

    printf("{?} Enter anime review: ");
    read_buf(new->review, REVIEW_MAX_SIZE);

    printf("{?} Enter anime score (0-100): ");
    int score = read_int();

    if (score < 0)
        new->score = 0;
    else if (score > 100)
        new->score = 100;
    else
        new->score = score;

    new->next = ListArray[idx]->head;
    ListArray[idx]->head = new;
    ListArray[idx]->size++;

    return 1;
};

int change_review(void)
{
    printf("{?} Enter list idx: ");
    int idx = read_int();

    if (idx < 0 || idx > LIST_MAX_SIZE) {
        puts("{-} Invalid idx!");
        return 0;
    }

    if (ListArray[idx] == NULL) {
        puts("{-} No such list!");
        return 0;
    }

    if (ListArray[idx]->size == 0) {
        puts("{-} This list is empty!");
        return 0;
    }

    printf("{?} Enter anime title to change review: ");
    char* title = (char*) malloc(TITLE_MAX_SIZE);
    read_buf(title, TITLE_MAX_SIZE);

    // find title in single-linked list
    AnimeEntry* current = ListArray[idx]->head;

    while (current != NULL) {
        if (!strcmp(title, current->title)) {
            printf("{?} Enter new review: ");
            read_buf(current->review, REVIEW_MAX_SIZE);
            return 1;
        }
        current = current->next;
    }

    puts("{-} No such anime in this list!");
    return 0;
};

int del_anime(void)
{
    printf("{?} Enter list idx: ");
    int idx = read_int();

    if (idx < 0 || idx > LIST_MAX_SIZE) {
        puts("{-} Invalid idx!");
        return 0;
    }

    if (ListArray[idx] == NULL) {
        puts("{-} No such list!");
        return 0;
    }

    if (ListArray[idx]->size == 0) {
        puts("{-} This list is empty!");
        return 0;
    }

    printf("{?} Enter anime title to delete: ");
    char* title = (char*) malloc(TITLE_MAX_SIZE);
    read_buf(title, TITLE_MAX_SIZE);

    // find title in single-linked list
    AnimeEntry* current = ListArray[idx]->head;

    while (current != NULL) {
        if (!strcmp(title, current->title)) {
            ListArray[idx]->size--;
            if (current == ListArray[idx]->head) {
                AnimeEntry* tmp = ListArray[idx]->head;
                ListArray[idx]->head = ListArray[idx]->head->next;
                free_entry(tmp);
                return 1;
            }

            delete_entry(ListArray[idx]->head, current);
            return 1;
        }
        current = current->next;
    }

    puts("{-} No such anime in this list!");
    return 0;
}

int view_list(void)
{
    printf("{?} Enter list idx: ");
    int idx = read_int();

    if (idx < 0 || idx > LIST_MAX_SIZE) {
        puts("{-} Invalid idx!");
        return 0;
    }

    if (ListArray[idx] == NULL) {
        puts("{-} No such list!");
        return 0;
    }

    if (ListArray[idx]->size == 0) {
        puts("{-} This list is empty!");
        return 0;
    }

    AnimeEntry* current = ListArray[idx]->head;

    int cnt = 0;
    printf("---- List [%d] ----\n", idx);

    while (current != NULL) {
        printf("Title #%d\n", cnt);
        puts("------------------");
        printf("Name: %s\n", current->title);
        printf("Review: %s\n", current->review);
        printf("Score: %d\n", current->score);
        puts("------------------");
        current = current->next;
        cnt++;
    }

    return 1;
};

int delete_entry(AnimeEntry* root, AnimeEntry* elem)
{
    AnimeEntry* current = root;

    while (current->next != elem) {
        current = current->next;
    }
    
    current->next = elem->next;
    free_entry(elem);

    return 1;
}

void free_entry(AnimeEntry* elem)
{
    free(elem->title);
    free(elem->review);
    free(elem);
};