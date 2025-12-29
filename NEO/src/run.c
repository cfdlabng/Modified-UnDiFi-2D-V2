/***************************************************************************
                                    run.c
                                    -----
      This is run: it drives the real computation through the real time loop
                            -------------------
    Code developed by M. Ricchiuto, Inria - mario.ricchiuto@inria.fr
 ***************************************************************************/
#include "common.h"

extern int initial_state, time_step, time_step_max, save_solution, info, counter_info,solver_mode  ;
int time_level; //vivek
extern double time, t_max, residual_norm, dt ;

extern void initialize_solution() ;
extern void compute_time_step() ;
extern void move_compute_save_the_mesh() ;
extern void pseudo_time_stepper() ;
extern void write_solution() ;
extern void element_preprocessing() ;

void run()
{
     int counter ;

//printf("maximum time %lf \n", t_max);
         printf( "\n" ) ;
         printf( "          *************************************\n" ) ;
         printf( "          *************************************\n" ) ;
         printf( "          **                                 **\n" ) ;
         printf( "          **             End of the          **\n" ) ;
         printf( "          **                                 **\n" ) ;
         printf( "          **        pre-processing phase     **\n" ) ;
         printf( "          **                                 **\n" ) ;
         printf( "          *************************************\n" ) ;
         printf( "          **                                 **\n" ) ;
         printf( "          ** The real computation starts.... **\n" ) ;
         printf( "          **                                 **\n" ) ;
         printf( "          *************************************\n" ) ;
         printf( "          *************************************\n" ) ;
         printf( "\n" ) ;
//printf("maximum nof time steps %ld \n", time_step_max);

         counter_info = 0 ;

         time_step = 0 ;

         counter = 0 ;

         time = 0.0 ;

         while ( ( t_max > time + small  )&&( time_step < time_step_max ) )
               {
	
                 time_step++ ;

                 counter ++ ;

                 counter_info ++ ;

                 initialize_solution() ;

                 compute_time_step() ;

                 move_compute_save_the_mesh() ;

		 element_preprocessing() ;

                 pseudo_time_stepper() ;

                 if ( counter_info == info )		
                 {
                   printf( "                   Time Iteration = %d            \n", time_step ) ;
                    printf( "                   Time Reached = %le            \n", time ) ;
                   printf( "\n" ) ;
                    const char *filename = NULL; //vivek
                    FILE *fp = NULL;
                    if (solver_mode == 0) //capturing
                    {   filename = "Capturing_convergence.dat"; //vivek
                        const char *mode = (time_step == 1) ? "w" : "a";
                        fp = fopen(filename, mode);
                        if (!fp) 
                        {
                        perror("Error opening convergence.dat");
                        exit(EXIT_FAILURE);
                        }
                        // If the file is empty, write the header
                        if (time_step == 1) 
                        {
                        fprintf(fp, "%-10s %-20s\n", "time_step", "LOG10( norm1_res )");
                        }
                        // Write Time Iteration and Time Reached
                        fprintf(fp, "%-10d %-20.6le\n", time_step, residual_norm);
                        fclose(fp);
                    }
                    else if (solver_mode == 1) //fitting
                    { 
                        filename = "fitting_convergence.dat"; //vivek
                        FILE *ft = fopen("time_level.dat", "r");
                        if (ft == NULL) 
                        {
                        perror("Error opening time_level.dat");
                        return 1;
                        }

                        if (fscanf(ft, "%d", &time_level) != 1) 
                        {
                        fprintf(stderr, "Error reading time_level\n");
                        fclose(ft);
                        return 1;
                        }
                        
                        const char *mode = (time_level == 1) ? "w" : "a";
                        fp = fopen(filename, mode);
                        if (!fp) 
                        {
                        perror("Error opening convergence.dat");
                        exit(EXIT_FAILURE);
                        }

                        if (time_level == 1) 
                        {
                        fprintf(fp, "%-10s %-20s\n", "time_step", "LOG10( norm1_res )");
                        }

                        fprintf(fp, "%-10d %-20.6le\n", time_level,residual_norm);
                        fclose(fp);
                    }//vivek
                    

                   counter_info = 0 ;
                 }

                if ( counter == save_solution )
                   {
                     counter = 0 ;

		 printf("Before write_solution\n");
                     write_solution() ;
                   }

/*******************************************************************/
/******* Below: sampling for the mach # wind tunnel ****************/
/*******************************************************************/
if ( initial_state == 3 ){
                if ( fabs( time - 0.5 ) < 0.00001 ) write_solution() ;    
                if ( fabs( time - 1. ) < 0.00001 ) write_solution() ;    
                if ( fabs( time - 1.5 ) < 0.00001 ) write_solution() ;    
                if ( fabs( time - 2. ) < 0.00001 ) write_solution() ;    
                if ( fabs( time - 2.5 ) < 0.00001 ) write_solution() ;    
                if ( fabs( time - 3. ) < 0.00001 ) write_solution() ;    
                if ( fabs( time - 3.5 ) < 0.00001 ) write_solution() ;    
                if ( fabs( time - 4. ) < 0.00001 ) write_solution() ;    
}
/*******************************************************************/
/******* Above: sampling for the mach # wind tunnel ****************/
/*******************************************************************/

/*******************************************************************/
/***** Below: sampling for wind tunnel with flap deflection  *******/
/*******************************************************************/
if ( initial_state == 13 ){
                if ( fabs( time - 0.20 ) < 0.0001 ) write_solution() ; //1   
                if ( fabs( time - 0.40 ) < 0.0001 ) write_solution() ; //2   
                if ( fabs( time - 0.60 ) < 0.0001 ) write_solution() ; //3   
                if ( fabs( time - 0.80 ) < 0.0001 ) write_solution() ; //4   
                if ( fabs( time - 1.00 ) < 0.0001 ) write_solution() ; //5
                if ( fabs( time - 1.20 ) < 0.0001 ) write_solution() ; //6 
                if ( fabs( time - 1.40 ) < 0.0001 ) write_solution() ; //7
                if ( fabs( time - 1.60 ) < 0.0001 ) write_solution() ; //8
                if ( fabs( time - 1.80 ) < 0.0001 ) write_solution() ; //9   
                if ( fabs( time - 2.00 ) < 0.0001 ) write_solution() ; //10   
                if ( fabs( time - 2.20 ) < 0.0001 ) write_solution() ; //11   
                if ( fabs( time - 2.40 ) < 0.0001 ) write_solution() ; //12
                if ( fabs( time - 2.50 ) < 0.0001 ) write_solution() ; //13 
}
/*******************************************************************/
/***** Above: sampling for wind tunnel with flap deflection  *******/
/*******************************************************************/
		
		
               }
// printf("Should NOT be here ");
}



