#include <iostream>
#include <string>
#include <WS2tcpip.h>
#pragma comment (lib, "ws2_32.lib")
using namespace std;
void main()
{
	int ketnoi = -1;
	char conhan = -1;
	struct sockaddr_in diachiserver;
	int bonhonhan;
	int datasend=0;
	WSADATA wsData;
	WORD phienban = MAKEWORD(2, 2);
	int wsOk = WSAStartup(phienban, &wsData);
	if (wsOk != 0)
	{
		cout << "Khong the khoi tao moi truong winsock" << endl;
		return;
	}
	else
	{
		cout << "Khoi tao moi truong thanh cong\n";
	}
	ketnoi = socket(AF_INET, SOCK_STREAM, 0);
	if (ketnoi == INVALID_SOCKET)
	{
		cout << "Khoi tao diem giao tiep that bai!";
		return;
	}

	diachiserver.sin_family = AF_INET;
	diachiserver.sin_port = htons(54000);
	inet_pton(AF_INET, "192.169.1.10", &diachiserver.sin_addr.S_un.S_addr);
	int  x = connect(ketnoi, (sockaddr*)&diachiserver, sizeof(diachiserver));
	if (x == SOCKET_ERROR)
	{
		cerr << "Khong the ket noi voi server, ma loi: " << WSAGetLastError() << endl;
		closesocket(ketnoi);
		WSACleanup();
		return;
	}
	else
	{
		cout << "Ket noi server thanh cong" << endl;
		bonhonhan = 3276;
		send(ketnoi, (char*)&bonhonhan, 2, 0);
		while (true)
		{
			recv(ketnoi, (char*)&datasend, 4, 0);//1 word
			printf("nhan duoc %d ", datasend);
			//closesocket(ketnoi);
		}
	}

}