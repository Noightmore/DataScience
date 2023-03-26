#include "../include/dictionary.h"

Table* dict_create_table(int capacity)
{
        Table* table = malloc(sizeof(Table));
        table->entries = calloc(capacity, sizeof(Entry*));
        table->size = 0;
        table->capacity = capacity;
        return table;
}

// obsolete
void dict_destroy_table(Table* table)
{
        for (int i = 0; i < table->capacity; i++)
        {
                Entry* entry = table->entries[i];
                while (entry != NULL)
                {
                        Entry* next = entry->next;
                        free(entry->key);
                        free(entry);
                        entry = next;
                }
        }
        free(table->entries);
        free(table);
}

int dict_hash(Table* table, char* key)
{
        int hash = 0;
        for (int i = 0; i < strlen(key); i++)
        {
                hash = hash * 31 + key[i];
        }
        return abs(hash % table->capacity);
}

Entry* dict_find_entry(Table* table, char* key)
{
        unsigned int index = dict_hash(table, key);
        Entry* entry = table->entries[index];
        while (entry != NULL)
        {
                if (strcmp(entry->key, key) == 0)
                {
                        return entry;
                }
                entry = entry->next;
        }
        return NULL;
}

void dict_set_entry(Table* table, char* key, int value)
{
        Entry* entry = dict_find_entry(table, key);
        if (entry != NULL)
        {
                entry->value = value;
                return;
        }

        int index = dict_hash(table, key);
        entry = malloc(sizeof(Entry));
        entry->key = strdup(key);
        entry->value = value;
        entry->next = table->entries[index];
        table->entries[index] = entry;
        table->size++;
}

int dict_get_entry(Table* table, char* key)
{
        Entry* entry = dict_find_entry(table, key);

        if (entry == NULL)
        {
                return -1;
        }

        return entry->value;
}

// obsolete
void dict_delete_entry(Table* table, char* key)
{
        int index = dict_hash(table, key);
        Entry* previous_entry = NULL;
        Entry* entry = table->entries[index];
        while (entry != NULL)
        {
                if (strcmp(entry->key, key) == 0)
                {
                        if (previous_entry == NULL)
                        {
                                table->entries[index] = entry->next;
                        }
                        else
                        {
                                previous_entry->next = entry->next;
                        }
                        free(entry->key);
                        free(entry);
                        table->size--;
                        return;
                }
                previous_entry = entry;
                entry = entry->next;
        }
}
