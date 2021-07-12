#define FLAG_PREFIX_LEN 25
#define STATES_COUNT 9
#define INITIAL_STATE 0
#define FINAL_STATE 8

typedef struct Node
{
    char from;
    char to;
    char next_state;
} Node;

void build_states(int cur_state, int flag_index);