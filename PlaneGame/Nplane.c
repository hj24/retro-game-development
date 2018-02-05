#include <stdio.h>
#include <stdlib.h>
#include <curses.h>            //unix/linux下代替conion.h（Windows下）的图形库
#include <time.h>
#include <termios.h>
#include <term.h>
#include <fcntl.h>
#include <unistd.h>
#include <locale.h>      
/*国家、文化和语言规则集称为区域设置，locale.h头文件中定义了区域设置相关的函数。使用这个函数避免中文输出出现乱码*/

static struct termios initial_settings, new_settings;
static int peek_character = -1;
void init_keyboard();
void close_keyboard();
int kbhit();
int readch();

//全局变量
int position_x,position_y;      //我方飞机位置
int bullet_x,bullet_y;          //子弹位置
int enemy_x,enemy_y;            //敌机位置
int height,width;               //画面尺寸
int count=0;                    //用来记算得分
int key=1;                      //用来结束游戏

void show();
void initial();
void startup();
void updatewithinput();
void updatewithoutinput();
void introduction();
void endgame();
int main(){
	int ch =0;
	startup();                  //数据初始化
	setlocale(LC_ALL,"");       //与locale配合使用，在初始化屏幕前设置
	initial();
	introduction();
	while(key){                   //游戏循环执行
		show();
		updatewithoutinput();
		refresh();              //刷新屏幕
		init_keyboard();
		updatewithinput();
		close_keyboard();
	}
	endwin();
	return 0;
}
void initial(){
	initscr();
	noecho();
	refresh();
}
void startup(){                                       //设置画面尺寸，敌我飞机以及子弹的位置
	height = 100;
	width = 60;
	position_x = height/2;
	position_y = width/2;
    bullet_x = -1;
	bullet_y = position_y;
	enemy_x = 0;
    enemy_y = position_y-1;
}
void updatewithinput(){                               //w a s d 分别控制 上 左 下 右 按空格发射子弹，q发射
	char input;
	if(kbhit()){
		input = readch();
		if(input=='a'){
			--position_y;
		}
		if(input=='d'){
			++position_y;
		}
		if(input=='w'){
			--position_x;
		}
		if(input=='s'){
			++position_x;
		}
		if(input==' '){
			bullet_x=position_x-1;
			bullet_y=position_y;
		}
		if(input=='q'){
			key=0;
		}
	}
}
void show(){
	int i,j,pj;
	clear();
	for(i=0;i<height;++i){
		for(j=0;j<width;++j){
			if((i==position_x)&&(j==position_y)){      //输出飞机
				printw("*\n");
				for(pj=0;pj<(position_y)-2;pj++){
					printw(" ");
				}
				printw("*****\n");
				for(pj=0;pj<(position_y)-1;pj++){
					printw(" ");
				}
				printw("* *");
			}else if((i==enemy_x)&&(j==enemy_y)){      //输出敌机
				printw("$");
			}else if((i==bullet_x)&&(j==bullet_y)){    //输出子弹
				printw("|");
			}else if((i==0)&&(j==width-6)){
				printw("得分是：%d",count);
			}else {
				printw(" ");
			}
		}
		printw("\n"); 
	}
}
void updatewithoutinput(){
	static int bullet_speed=0;
	if(bullet_speed<60){
		bullet_speed++;
	}
	if(bullet_speed==60){
	if(bullet_x>-1){                                   //用来更新子弹的显示
		bullet_x --;
		bullet_speed=0;
	}
	}
	if((enemy_x==bullet_x)&&(enemy_y==bullet_y)){      //用来判断是否击中低级并计算得分
		count++;
		bullet_x= -1;                                  //子弹失效
		enemy_x= 0;                                    //产生新的敌机
		srand((unsigned)time(0));
		enemy_y=rand()%width;
	}else if(enemy_x>height){                          //敌机跑出显示屏幕
		enemy_x=0;
		srand((unsigned)time(0));
        enemy_y=rand()%width;
	}else if(bullet_x<0){
		bullet_x= -1;
	}
	static int enemy_speed=0;                                //用来显示敌机的更新，引入局部静态变量表示速度
	if(enemy_speed<100){
		enemy_speed++;
	}
	if(enemy_speed==100){
		enemy_x ++;
		enemy_speed=0;
	}
}

//下面是检测函数kbhit在unix/linux上的实现

void init_keyboard()
{
	tcgetattr(0,&initial_settings);
	new_settings = initial_settings;
	new_settings.c_lflag &= ~ICANON;
	new_settings.c_lflag &= ~ECHO;
	new_settings.c_lflag &= ~ISIG;
	new_settings.c_cc[VMIN] = 1;
	new_settings.c_cc[VTIME] = 0;
	tcsetattr(0, TCSANOW, &new_settings);
}
void close_keyboard()
{
	tcsetattr(0, TCSANOW, &initial_settings);
}

int kbhit()
{
	char ch;
	int nread;
	if(peek_character != -1)
	    return 1;
	    new_settings.c_cc[VMIN]=0;
	    tcsetattr(0, TCSANOW, &new_settings);
		nread = read(0,&ch,1);
		new_settings.c_cc[VMIN]=1;
		tcsetattr(0, TCSANOW, &new_settings);
		if(nread == 1) {
		    peek_character = ch;
			return 1;
		}
		return 0;
}
int readch()
{
	char ch;
	if(peek_character != -1) {
		ch = peek_character;
		peek_character = -1;
		return ch;
	}
	read(0,&ch,1);
	return ch;
}
void introduction(){
	int i,j;
	for(i=0;i<height/4;i++){
		printw("\n");
		for(j=0;j<width/2;j++){
			printw(" ");
		}
	}
	printw("这是一个字符界面的飞机游戏\n");
	for(j=0;j<width/2;j++){
		printw(" ");
	}
    printw("w,s,a,d分别对应上下左右,q退出\n");
	for(j=0;j<width/2;j++){
		printw(" ");
	}
	printw(" 按任意键继续\n");
	refresh();
    getch();
    clear();
}
