#ifndef TGHE_SEMESTRAL_DICTIONARY_H
#define TGHE_SEMESTRAL_DICTIONARY_H

#include <stdlib.h>
#include <string.h>

typedef struct entry_t
{
    char* key;
    struct entry_t** entries;
    struct entry_t* next;

} Entry;

typedef struct
{
    Entry** entries;
    int size;
    int capacity;

} Table;


Table* dict_create_table(int capacity);

// obsolete
// TODO: REMOVE
void dict_destroy_table(Table* table);

int dict_hash(Table* table, char* key);

Entry* dict_find_entry(Table* table, char* key);

void dict_set_entry(Table* table, char* key, int value);

int dict_get_entry(Table* table, char* key);

// obsolete
// TODO: REMOVE
void dict_delete_entry(Table* table, char* key);


#endif //TGHE_SEMESTRAL_DICTIONARY_H
