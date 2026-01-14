#include <stdio.h>
#include <string.h>
#include <windows.h>
#include <stdbool.h>
#define MAXN 1000

int output(int ei, int ej, int ansArray[MAXN + 2][MAXN + 2], int n, int m, int a, int b);
int condition(int a, int b,bool c);
char board[MAXN + 2][MAXN + 2];
int ans[MAXN + 2][MAXN + 2];
int prevX[MAXN + 2][MAXN + 2];
int prevY[MAXN + 2][MAXN + 2];
int pathMap[MAXN+2][MAXN+2];
typedef struct { int x, y; } Node;
Node queue[MAXN * MAXN + 5];
int head = 0, tail = 0;

int dir[4][2] = { {-1,0},{1,0},{0,-1},{0,1} };

int output(int ei, int ej, int ansArray[MAXN + 2][MAXN + 2], int n, int m, int cond, int steps){
    
    condition(cond, steps,false);
    FILE *fp = fopen("output.txt", "w");
    for(int i=1;i<=n;i++){
        for(int j=1;j<=m;j++){
            if(i==ei && j==ej) fprintf(fp,"%3s","E");
            else fprintf(fp,"%5d",ansArray[i][j]);
    }
    fprintf(fp,"\n");
    }
    fclose(fp);
    condition(cond, steps,true);
    return 0;
}
int condition(int a, int b, bool final){
    FILE *fp = fopen("condition.txt", "w");
    int tmp;
    tmp = final ? 1 : 0;
    fprintf(fp,"%d,%d,%d\n",a,b,tmp);
    fclose(fp);
    return 0;
}
int main() {
    int n = 33, m = 33; // 固定大小

    const char *input[] = {
        "111111111111111111111111111111111",
        "100000000000010000000000000000001",
        "101111111110111011111111111111101",
        "101000000010001010001000100000001",
        "101010111111101010101010101111101",
        "100010100000101000100010101000101",
        "111110101110101011111110101010101",
        "100000101010000000000010101010101",
        "101111101011111111111010101010101",
        "101000001000000000000010101010101",
        "101011111010111111111010101010101",
        "101010000010100000001010101010101",
        "101010111010101111101010101010101",
        "101010001010100000001000101010101",
        "101011101011101111111110101110101",
        "10100000001000100E000010100010101",
        "101110111010101000111011111010101",
        "100010000010101000101000000010101",
        "111011111110101111101111111110101",
        "100010000010101000001000001000101",
        "101110111010101011101011101011101",
        "101000001000001000101000101000101",
        "101011101111101110101110101110101",
        "101010001000000000101000100000101",
        "101010101010101111101011111111101",
        "100010101010100000101000001000001",
        "111110101011111110101111101011111",
        "100000101010000010100000101010001",
        "101111101010111010111110101010101",
        "100000001010001010000010001000101",
        "101011111011101011111011111011101",
        "1S1000000000001000001000000000001",
        "111111111111111111111111111111111"
    };
    int si=-1,sj=-1,ei=-1,ej=-1;

    for(int i=1;i<=n;i++){
        strcpy(board[i]+1, input[i-1]);
        for(int j=1;j<=m;j++){
            if(board[i][j]=='S'){si=i; sj=j; board[i][j]='0';}
            else if(board[i][j]=='E'){ei=i; ej=j; board[i][j]='0';}
            else if(board[i][j]!='0' && board[i][j]!='1'){printf("輸入錯誤\n"); return 1;}
            prevX[i][j] = prevY[i][j] = -1;
        }
        board[i][0] = board[i][m+1] = '1';
    }
    for(int j=0;j<=m+1;j++) board[0][j]=board[n+1][j]='1';

    for(int i=1;i<=n;i++)
        for(int j=1;j<=m;j++)
            ans[i][j] = -1;
    ans[si][sj] = 0;
    // for(int i=0;i<(MAXN+2);i++){
    //     for (int j=0;j<MAXN+2;j++){
    //         if (board[i][j]=='S' || board[i][j]=='E'){
    //             ans[i][j]=1;
    //         } else {
    //             ans[i][j]=board[i][j]=='1' ? -1 : 0;
    //         }
    //     }
    // }
    queue[tail++] = (Node){si,sj};

    while(head<tail){
        Node cur = queue[head++];
        int x=cur.x,y=cur.y;
        for(int k=0;k<4;k++){
            int nx = x+dir[k][0], ny=y+dir[k][1];
            if(board[nx][ny]=='1' || ans[nx][ny]!=-1) continue;
            ans[nx][ny] = ans[x][y]+1;
            prevX[nx][ny] = x; prevY[nx][ny] = y;
            queue[tail++] = (Node){nx,ny};
        }
        //輸出到檔案
        output(ei,ej,ans,n,m,ans[cur.x][cur.y],head);

        Sleep(150);
        printf("step%d\n",head);
    }

    if(ans[ei][ej]==-1){
        printf("無法到達終點\n");
        return 0;
    }

    // 輸出距離矩陣，終點顯示E
    printf("距離矩陣：\n");
    for(int i=1;i<=n;i++){
        for(int j=1;j<=m;j++){
            if(i==ei && j==ej) printf("%5s","E");
            else printf("%5d",ans[i][j]);
        }
        printf("\n");
    }

    printf("最短步數：%d\n", ans[ei][ej]);

    // 生成最短路徑圖

    for(int i=1;i<=n;i++)
        for(int j=1;j<=m;j++)
            pathMap[i][j] = -1;

    int x=ei,y=ej;
    while(!(x==si && y==sj)){
        pathMap[x][y] = 0;
        int tx=prevX[x][y], ty=prevY[x][y];
        x=tx; y=ty;
    }
    pathMap[si][sj]=0;
    printf("\n");
    //final output 
    printf("最短路徑圖：\n");
    FILE *fp = fopen("output.txt", "w");
    for(int i=1;i<=n;i++){
        for(int j=1;j<=m;j++)
            printf("%5d",pathMap[i][j]);
        printf("\n");
    }
    for(int i=1;i<=n;i++){
        for(int j=1;j<=m;j++)
            fprintf(fp,"%5d",pathMap[i][j]);
        fprintf(fp,"\n");
    }
    fclose(fp);
    return 0;
}

