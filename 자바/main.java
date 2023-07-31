import java.util.Scanner;
import javax.swing.*;
import java.awt.*;



class GFG
{
// midPoint function for line generation
static void midPoint(int X1, int Y1, int X2, int Y2)
{
    // calculate dx & dy
    int dx = X2 - X1;
    int dy = Y2 - Y1;
    // initial value of decision
    // parameter d
    int d = dy*2-dx;
    int incrE=dy*2;
    int incrNE=(dy-dx)*2;

    int x = X1, y = Y1;

    System.out.print(x +"," + y + "\n");
 
    // iterate through value of X
    while (x < X2)
    {
    
        if(d<=0){
            d+=incrE;
            x++;
        }
        else{
            d+=incrNE;
            x++;
            y++;
        }
        System.out.print(x +"," + y + "\n");
    }
}
 
// Driver code
public static void main (String[] args)
{
    int X1,X2,Y1,Y2;
    Scanner sc = new Scanner(System.in);
    
    System.out.print("x1 : ");
	X1 = sc.nextInt();
    System.out.print("Y1 : ");
	Y1 = sc.nextInt();
    System.out.print("X2 : ");
	X2 = sc.nextInt();
    System.out.print("Y2 : ");
	Y2 = sc.nextInt();

    midPoint(X1, Y1, X2, Y2);


}
}
