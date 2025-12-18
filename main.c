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
            else fprintf(fp,"%3d",ansArray[i][j]);
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
    int n = 17, m = 17; // 固定大小

    // 直接把輸入資料寫在字串陣列
    const char *input[] = {
        "11111111111111111",
        "S0000010001000001",
        "10111010101011101",
        "10100010101010001",
        "10101110101010111",
        "10100000100010001",
        "10111111101110101",
        "10100000101000101",
        "10101110101011101",
        "10000010101010001",
        "11111010101010101",
        "10000010001010101",
        "10111111111010101",
        "10100000000010101",
        "10111111111110101",
        "10000000000000101",
        "111111111111111E1"
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
            if(i==ei && j==ej) printf("%3s","E");
            else printf("%3d",ans[i][j]);
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
            printf("%2d",pathMap[i][j]);
        printf("\n");
    }
    for(int i=1;i<=n;i++){
        for(int j=1;j<=m;j++)
            fprintf(fp,"%3d",pathMap[i][j]);
        fprintf(fp,"\n");
    }
    fclose(fp);
    return 0;
}

