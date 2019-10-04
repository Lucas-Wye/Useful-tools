#include<iostream>
#include<vector>
#include<fstream>
#include<string>
#include<iterator>
using namespace std;

class userinfo{
public:
	string name;
	string phone;
	friend istream &operator>>(istream&i, userinfo &u);
	friend ostream &operator<<(ostream &o, userinfo &u);
};

ostream & operator <<(ostream &o, userinfo &u){
	o << u.phone << "\t" << u.name << endl;
	return o;
}

istream & operator >>(istream &i, userinfo &u){
	i >> u.phone >> u.name;
	return i;
}

int main(int agrc, char** argv){
	vector<userinfo>v;
	vector<string>s;
	ifstream in("input.txt");
	ofstream out("output.vcf");
	copy(istream_iterator<userinfo>(in), istream_iterator<userinfo>(), back_inserter(v));
	/*
		BEGIN:VCARD
		VERSION:3.0
		N:;XX;;;
		FN:XX
		TEL;TYPE=CELL:13012341234
		END:VCARD
	*/
	for (int i=0;i<v.size();i++){
		string buf = string("BEGIN:VCARD\n") + "VERSION:3.0\n" + "N:;"+v[i].name+";;;\n" + "FN:"+v[i].name+"\n" + "TEL;TYPE=CELL:"+v[i].phone+"\n" + "END:VCARD\n";
		cout << buf << endl;
		s.push_back(buf);
	}
	ostream_iterator<string>it_tofile(out);
	copy(s.begin(),s.end(),it_tofile);
	in.close();
	out.close();
	cin.get();
}
