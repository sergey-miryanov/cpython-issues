import os, _winapi
han = _winapi.OpenProcess(_winapi.PROCESS_QUERY_INFORMATION | _winapi.PROCESS_VM_READ, 0, os.getpid())
process_memory = int(_winapi.GetProcessMemoryInfo(han)['WorkingSetSize'])

print(process_memory)
