#include "include/matrix_tools.h"
#include "include/test_tools.h"

int main()
{
    matrix_data *m_data = initialize_matrix();
    print_connection_matrix_to_stdout(m_data);


    return 0;
}
