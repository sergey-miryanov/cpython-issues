#include <Python.h>

void func()
{
    Py_Initialize(); Py_Finalize();
    Py_ssize_t cnt = _Py_GetRefTotal();
    printf("sys.gettotalrefcount(): %zd\n", cnt);
}

int main(int argc, char *argv[])
{
    Py_SetProgramName(L"./_testembed");
    for (int i=0; i < 10; i++) {
        func();
    }
}
