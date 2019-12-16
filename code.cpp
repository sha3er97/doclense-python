
#include<iostream>
#include <fstream>

using namespace std;
int main() {
	ofstream myfile;
  	myfile.open ("letter.txt");
	for (int i = 0; i < 1500; i++) {
		myfile  << "9" << "  ";
	}
	myfile.close();
}