#include "basic_tests.h"

void test_dictionary()
{
        Table* table = dict_create_table(10);

        // Test set_entry() and get_entry()
        dict_set_entry(table, "key1", 42);
        assert(dict_get_entry(table, "key1") == 42);
        dict_set_entry(table, "key2", 1234);
        assert(dict_get_entry(table, "key2") == 1234);
        dict_set_entry(table, "key3", -1);
        assert(dict_get_entry(table, "key3") == -1);

        // Test delete_entry()
        dict_delete_entry(table, "key2");
        assert(dict_get_entry(table, "key2") == -1);
        dict_delete_entry(table, "key1");
        assert(dict_get_entry(table, "key1") == -1);

        // Test resizing of the table
        for (int i = 0; i < 1000; i++)
        {
                char key[10];
                sprintf(key, "key%d", i);
                dict_set_entry(table, key, i);
        }
        assert(dict_get_entry(table, "key123") == 123);
        assert(dict_get_entry(table, "key999") == 999);

        dict_destroy_table(table);

        Table* table2 = dict_create_table(10);

        // Test dict_set_entry() and dict_get_entry()
        dict_set_entry(table2, "foo", 42);
        dict_set_entry(table2, "bar", 123);
        dict_set_entry(table2, "baz", 789);

        assert(dict_get_entry(table2, "foo") == 42);
        assert(dict_get_entry(table2, "bar") == 123);
        assert(dict_get_entry(table2, "baz") == 789);
        assert(dict_get_entry(table2, "qux") == -1);

        // Test dict_delete_entry()
        dict_delete_entry(table2, "bar");

        assert(dict_get_entry(table2, "bar") == -1);

        // Test dict_destroy_table()
        dict_destroy_table(table2);
        printf("All tests passed!\n");
}
