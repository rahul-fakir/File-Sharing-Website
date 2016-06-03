#include <iostream>
#include <fstream>
#include <string>
using namespace std;
// ������� �������� ���������� � ������
// name author year lans
struct book
{
	char name[100], author[100];
	int year, lands;
};
/*��������� "�����":
��������;
�����;
��� �������;
���������� �������.
������� 3 �������� �� ������ �����, �������� ������� ����� ��������� � ��������� ���������.
*/

//����� ����� ����������� �����
bool vivod(char path[]) // ������� ������ �� �����
{
	fstream f(path, ios::in); // ������� �� ������ ����
	if (!f)
	{
		cout << "������ ������ �����! ��������� ��� ���� ����������!";
		f.close();
		return false;
	}
	book* el = new book;
	f >> el->name >> el->author >> el->year >> el->lands;
	cout << el->name << endl << el->author << endl << el->year << endl << el->lands << endl << endl;
	while (!f.eof())
	{
		f >> el->name >> el->author >> el->year >> el->lands;
		cout << el->name << endl << el->author << endl << el->year << endl << el->lands << endl << endl;
	}

	delete el;
	f.close();
	return true;
}


//�������� ����� �� ����������
bool first(char path[])
{
	book* el = new book;
	fstream f(path, ios::out); // ��������� ���� �� ������ ���� ����������
	if (!f)
	{
		cout << "������ ������ �����! ��������� ��� ���� ����������!";
		return false;
	}
	int kol = 0;// ��� �� ������ ������ ������ ��� ���. ������� ������ ���������� ��� ������ ������ � ��� ���������
	while (true)
	{
		cout << "\n�������� ���������? y\n \n-->";
		char c;
		cin >> c;
		if (c == 'y')
		{
			cout << "\n������� ��� �����\n-->";
			cin >> el->name;
			cout << "������� ������ �����\n-->";
			cin >> el->author;
			cout << "������� ��� �������\n-->";
			cin >> el->year;
			cout << "������� ���-�� �������\n-->";
			cin >> el->lands;
			if (kol == 0)// ���� ������ ������
			{
				f << el->name << " " << el->author << " " << el->year << " " << el->lands;
			}
			else//���� �� ������ ������
			{
				f << endl << el->name << " " << el->author << " " << el->year << " " << el->lands;
			}
			kol++;//��������� ���-�� �����
		}
		else if (c == 'n')
		{
			f.close();
			delete el;
			return true;
		}
	}
}

//���������� ������ �������� ����� ������
bool add(book* newB, int number, char path[])//number- ����� ������ ����� ������� ��������, ������ ���� � 0
{
	fstream fRead(path, ios::in); // ������� �� ������ ����
	fstream fWrite("BufFile.txt", ios::out); // ��������� ���� �� ������ ���� ����������
	if (!fRead || !fWrite)
	{
		cout << "������ ������ �����! ��������� ��� ���� ����������!";
		fRead.close();
		fWrite.close();
		return false;
	}
	book* el = new book;
	int kol = 0;
	//fRead >> el->name >> el->author >> el->year >> el->lands;
	while (!fRead.eof()) 
	{
		fRead >> el->name >> el->author >> el->year >> el->lands;
		//���������, ��� �� ��� ���� �������� ������???
		if (kol == number)
		{
			if (kol == 0)
				fWrite << newB->name << " " << newB->author << " " << newB->year << " " << newB->lands;
			else
				fWrite << endl << newB->name << " " << newB->author << " " << newB->year << " " << newB->lands;
			kol++;
			cout << kol << endl;
		}

		//�������� ������� ������
		if (kol == 0)// ���� ������ ������
		{
			fWrite << el->name << " " << el->author << " " << el->year << " " << el->lands;
			cout << kol << endl;
		}
		else//���� �� ������ ������
		{
			fWrite << endl << el->name << " " << el->author << " " << el->year << " " << el->lands;
			cout << kol << endl;
		}
		kol++;//��������� ���-�� �����
	}
	fRead.close();
	fWrite.close();
	delete el;
	//��� ������� �������������
	remove(path);//������� ������ ����
	rename("BufFile.txt", path);//������������� ����� ����
	return true;
}


//������� ���������� ��� ���������
bool equalBook(book* one, book* two)
{
	if (strcmp(one->name, two->name) == 0)
	if (strcmp(one->author, two->author) == 0)
	if (one->year == two->year)
	if (one->lands == two->lands)
		return true; // ���� ������ ��� 4 ��������, �� ��� �����
	return false;// ����� �� �����
}


//����� � �����, ���������� ����� ������ ���������� �������� ������� � 0. ���� �� �������, ���������� -1.
int find(book* findBook, char path[]) // ���� �� ������ ���������. �.�. ������ ������ �� ������ ������� ��������� ��������� � findBook
{
	fstream f(path, ios::in); // ������� �� ������ ����
	book* el = new book;
	if (!f)
	{
		cout << "������ ������ �����! ��������� ��� ���� ����������!";
		f.close();
		return false;
	}
	//�������� ������ ������� �� ������������
	f >> el->name >> el->author >> el->year >> el->lands;
	if (equalBook(findBook, el)) // ���� ��� �����
	{
		f.close();
		delete el;
		return 0;
	}
	//���� ������ �� ����� ��������, �� ��������� �� ����� ����� ������
	int kol = 1;
	while (!f.eof())
	{
		f >> el->name >> el->author >> el->year >> el->lands;
		if (equalBook(findBook, el))
		{
			f.close();
			delete el;
			return kol;
		}
		kol++;
	}
	//���� �� ����� �� ������ ���������� �� ������ -1
	f.close();
	delete el;
	return -1;
}


//����� ������� �������� ������ �������� �� �����
bool delBook(char path[], int number) // number ����� ������ ������� ���� �������, ������� � 0.
{
	fstream fRead(path, ios::in); // ������� �� ������ ����
	fstream fWrite("BufFile.txt", ios::out); // ��������� ���� �� ������ ���� ����������
	if (!fRead || !fWrite)
	{
		cout << "������ ������ �����! ��������� ��� ���� ����������!";
		fRead.close();
		fWrite.close();
		return false;
	}
	book* el = new book;
	int kol = 0;
	while (!fRead.eof())
	{
		fRead >> el->name >> el->author >> el->year >> el->lands;
		if (kol != number)
			fWrite << el->name << " " << el->author << " " << el->year << " " << el->lands;
		kol++;
	}
	fRead.close();
	fWrite.close();
	delete el;
	//��� ������� �������������
	remove(path);//������� ������ ����
	rename("BufFile.txt", path);//������������� ����� ����
	return true;
}


//������� �������� ���� ������ ��������� �� �����. ���������� ������� ��������
bool delBook(char path[])
{
	fstream fRead(path, ios::in); // ������� �� ������ ����
	fstream fWrite("BufFile.txt", ios::out); // ��������� ���� �� ������ ���� ����������
	if (!fRead || !fWrite)
	{
		cout << "������ ������ �����! ��������� ��� ���� ����������!";
		fRead.close();
		fWrite.close();
		return false;
	}
	book* el = new book;
	int kol = 0;
	while (!fRead.eof())
	{
		fRead >> el->name >> el->author >> el->year >> el->lands;
		if (kol > 2)
			fWrite << el->name << " " << el->author << " " << el->year << " " << el->lands;
		kol++;
	}
	fRead.close();
	fWrite.close();
	delete el;
	//��� ������� �������������
	remove(path);//������� ������ ����
	rename("BufFile.txt", path);//������������� ����� ����
	return true;
}

void main()
{
	setlocale(0, "");
	first("basa.txt");
	vivod("basa.txt"); // �����
	book* e = new book;
	cin >> e->name >> e->author;
	e->year = 1875;
	e->lands = 56;
	add(e, 2, "basa.txt"); //������� ����� 2-� ��������� ������� e
	delBook("basa.txt"); // ������ ������ 3
	delBook("basa.txt", find(e, "basa.txt")); // ������ ������ ��������� �������, ������� ��������� � e
	system("pause");
}