#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <set>

using namespace std;

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/


int main()
{
    vector<vector<vector<vector<int> > > >  board( 3, vector<vector<vector<int> > >( 3, vector<vector<int> >(3, vector<int>( 3, false ) ) )) ;
    // game loop
    while (1) {
        int opponent_row;
        int opponent_col;
        int opponent_sub_row;
        int opponent_sub_col;

        cin >> opponent_row >> opponent_col >> opponent_sub_row >> opponent_sub_col; cin.ignore();

        // board[opponent_row / 3]
        // int valid_action_count;
        // cin >> valid_action_count; cin.ignore();
        // for (int i = 0; i < valid_action_count; i++) {
        //     int row;
        //     int col;
        //     cin >> row >> col; cin.ignore();
        // }

        // Write an action using cout. DON'T FORGET THE "<< endl"
        // To debug: cerr << "Debug messages..." << endl;
        cerr << "waiting" << endl;
        bool    found = false;

        for ( int i=0; i<3 and !found; i++ )
        {
            for ( int j=0; j<3 and !found; j++ )
            {
                for ( int k=0; k<3 and !found; k++ )
                {
                    for ( int l=0; l<3 and !found; l++ )
                    {
                        if ( board[i][j][k][l] != 0 )
                        {
                            found = true;
                            cout << i << j << k << l << endl;
                            board[i][j][k][l] = true;
                            break ;
                        }
                    }
                }
            }
        }
    }
}