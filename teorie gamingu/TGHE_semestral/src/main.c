#include "./unit_tests/tester.h"
#include "./include/app.h"
int main()
{
        int status;
        status = run_all_tests();
        //status = app_run();
        return status;
}
