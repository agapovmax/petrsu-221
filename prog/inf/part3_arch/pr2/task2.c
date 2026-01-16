// Предполагая: eax = n, ebx = 1


int main()
{
	int eax = 5;
	int ebx = 1;
	while (eax != 0)
	{
    		ebx = ebx * eax;
    		eax = eax - 1;
	}

	return eax;
}
