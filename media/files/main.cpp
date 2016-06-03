#include <iostream>
#include <fstream>
#include <string>
using namespace std;
// порядок хранения информации в строке
// name author year lans
struct book
{
	char name[100], author[100];
	int year, lands;
};
/*Структура "Книга":
название;
автор;
год издания;
количество страниц.
Удалить 3 элемента из начала файла, добавить элемент перед элементом с указанным названием.
*/

//вывод всего содержимого файла
bool vivod(char path[]) // функция вывода из файла
{
	fstream f(path, ios::in); // открыли на чтение файл
	if (!f)
	{
		cout << "ошибка чтения файла! Убедитесь что файл существует!";
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


//создание файла со структурой
bool first(char path[])
{
	book* el = new book;
	fstream f(path, ios::out); // открываем файл на запись либо перезапись
	if (!f)
	{
		cout << "ошибка чтения файла! Убедитесь что файл существует!";
		return false;
	}
	int kol = 0;// что бы понять первая строка или нет. Вариант записи отличается для первой строки и все остальных
	while (true)
	{
		cout << "\nДобавить структуру? y\n \n-->";
		char c;
		cin >> c;
		if (c == 'y')
		{
			cout << "\nВведите имя книги\n-->";
			cin >> el->name;
			cout << "Введите автора книги\n-->";
			cin >> el->author;
			cout << "Введите год издания\n-->";
			cin >> el->year;
			cout << "Введите кол-во страниц\n-->";
			cin >> el->lands;
			if (kol == 0)// если первая строка
			{
				f << el->name << " " << el->author << " " << el->year << " " << el->lands;
			}
			else//если не первая строка
			{
				f << endl << el->name << " " << el->author << " " << el->year << " " << el->lands;
			}
			kol++;//увеличили кол-во строк
		}
		else if (c == 'n')
		{
			f.close();
			delete el;
			return true;
		}
	}
}

//добавление одного элемента после номера
bool add(book* newB, int number, char path[])//number- номер строки после которой добавить, отсчет идет с 0
{
	fstream fRead(path, ios::in); // открыли на чтение файл
	fstream fWrite("BufFile.txt", ios::out); // открываем файл на запись либо перезапись
	if (!fRead || !fWrite)
	{
		cout << "ошибка чтения файла! Убедитесь что файл существует!";
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
		//проверяем, тут ли нам надо запистаь строку???
		if (kol == number)
		{
			if (kol == 0)
				fWrite << newB->name << " " << newB->author << " " << newB->year << " " << newB->lands;
			else
				fWrite << endl << newB->name << " " << newB->author << " " << newB->year << " " << newB->lands;
			kol++;
			cout << kol << endl;
		}

		//записали текущую строку
		if (kol == 0)// если первая строка
		{
			fWrite << el->name << " " << el->author << " " << el->year << " " << el->lands;
			cout << kol << endl;
		}
		else//если не первая строка
		{
			fWrite << endl << el->name << " " << el->author << " " << el->year << " " << el->lands;
			cout << kol << endl;
		}
		kol++;//увеличили кол-во строк
	}
	fRead.close();
	fWrite.close();
	delete el;
	//тут удалить переименовать
	remove(path);//удалили старый файл
	rename("BufFile.txt", path);//переименовали новый файл
	return true;
}


//функция сравнивает две структуры
bool equalBook(book* one, book* two)
{
	if (strcmp(one->name, two->name) == 0)
	if (strcmp(one->author, two->author) == 0)
	if (one->year == two->year)
	if (one->lands == two->lands)
		return true; // если прошли все 4 проверки, то они равны
	return false;// иначе не равны
}


//поиск в файле, возвращает номер строки найденного элемнета начиная с 0. Если не найдено, возвращает -1.
int find(book* findBook, char path[]) // ищем по полной структуре. Т.е. вернет только ту строку которая полностью совпадает с findBook
{
	fstream f(path, ios::in); // открыли на чтение файл
	book* el = new book;
	if (!f)
	{
		cout << "ошибка чтения файла! Убедитесь что файл существует!";
		f.close();
		return false;
	}
	//проверим первый элемент на одинаковость
	f >> el->name >> el->author >> el->year >> el->lands;
	if (equalBook(findBook, el)) // если они равны
	{
		f.close();
		delete el;
		return 0;
	}
	//если первый не равен искомому, то проверяем по всему файлу дальше
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
	//если не нашли ни одного совпадения то вернем -1
	f.close();
	delete el;
	return -1;
}


//Общая функция удаления любого элемнета из файла
bool delBook(char path[], int number) // number номер строки которую надо удалить, начиная с 0.
{
	fstream fRead(path, ios::in); // открыли на чтение файл
	fstream fWrite("BufFile.txt", ios::out); // открываем файл на запись либо перезапись
	if (!fRead || !fWrite)
	{
		cout << "ошибка чтения файла! Убедитесь что файл существует!";
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
	//тут удалить переименовать
	remove(path);//удалили старый файл
	rename("BufFile.txt", path);//переименовали новый файл
	return true;
}


//функция удаления трех первых элементов из файла. Перегрузка функции удаления
bool delBook(char path[])
{
	fstream fRead(path, ios::in); // открыли на чтение файл
	fstream fWrite("BufFile.txt", ios::out); // открываем файл на запись либо перезапись
	if (!fRead || !fWrite)
	{
		cout << "ошибка чтения файла! Убедитесь что файл существует!";
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
	//тут удалить переименовать
	remove(path);//удалили старый файл
	rename("BufFile.txt", path);//переименовали новый файл
	return true;
}

void main()
{
	setlocale(0, "");
	first("basa.txt");
	vivod("basa.txt"); // вывод
	book* e = new book;
	cin >> e->name >> e->author;
	e->year = 1875;
	e->lands = 56;
	add(e, 2, "basa.txt"); //добавит перед 2-м элементов едемент e
	delBook("basa.txt"); // удалит первых 3
	delBook("basa.txt", find(e, "basa.txt")); // удалит первый найденный элемнет, который совпадает с e
	system("pause");
}