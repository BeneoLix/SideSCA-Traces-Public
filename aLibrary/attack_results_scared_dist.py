import matplotlib.pyplot as _plt
import IPython.display as _display
import numpy as _np
import math as _math
import scared

figure_axes_text_size = 14
graph_title_fontsize = 14

RED_TEXT = '\033[31m'
GREEN_TEXT = '\033[32m'

color_all_guesses = 'grey'
color_best_guess = 'green'
color_right_guess = 'dodgerblue'

class attack_results_scared_dist():

    """
    This class is used to analyse the scared distinguishers operations
        - plot
        - remaining entropy
        - remaining entropy naive
        - options are provided to save the figures in these 3 functions

        - print_best_scores
        - print_scores

        - save results

    - args:
        - attack_object: the attack object to use
        - figure_name_path: the path and name of the file to use for storage of figures of results if defined and not None.        
        - file_name_path: the path and name of the file to use for storage of full results if defined and not None.
    """
    
    def __init__(self, attack_object, figure_name_path=None, file_name_path=None):
        self.attack_object = attack_object
        self.attack_object_convergence_step = attack_object.convergence_step
        self.attack_object_convergence_traces = attack_object.convergence_traces
        self.attack_object_results = attack_object.results
        self.attack_object_scores = attack_object.scores
        self.attack_object_processed_traces =  attack_object.processed_traces
        self.figure_name_path = figure_name_path
        self.file_name_path = file_name_path 

    def _plot_single_byte(self, key_byte, correct_key, do_not_save_figure_bool):
        DOWNS_STEP = 1
        guesses_number = self.attack_object_results.shape[0]
        best_guesses = self.attack_object_scores.argmax(0).squeeze()

        if self.attack_object_convergence_step is not None:
            CONV_POINTS =  self.attack_object_convergence_traces.shape[2]

            # Plot result traces
            _plt.subplot(1,3,1)
            for i in range(guesses_number): _plt.plot(self.attack_object_results[i,key_byte].T[:-1:DOWNS_STEP], color = color_all_guesses)
            _plt.plot(self.attack_object_results[best_guesses[key_byte],key_byte].T[:-1:DOWNS_STEP], color = color_best_guess, label='best score')
            if correct_key is not None: 
                _plt.plot(self.attack_object_results[correct_key[key_byte],key_byte].T[:-1:DOWNS_STEP], color = color_right_guess, label='right key')
            # Set axes and legend
            _plt.xticks(size = figure_axes_text_size)
            _plt.xlabel('time', size = figure_axes_text_size)
            _plt.yticks(size = figure_axes_text_size)
            _plt.ylabel('score', size = figure_axes_text_size)
            _plt.title('Attack traces results byte '+str(key_byte), size = figure_axes_text_size)
            _plt.legend(loc="best")

            #plot results in bar chart
            _plt.subplot(1,3,2)        
            s = self.attack_object_scores[:, key_byte]
            _plt.bar(range(len(s)),s, color=color_all_guesses)
            _plt.bar(best_guesses[key_byte], s[best_guesses[key_byte]], color=color_best_guess) 
            if correct_key is not None:  
                _plt.bar(correct_key[key_byte], s[correct_key[key_byte]], color=color_right_guess) 
            _plt.ylim((_np.min(s), _np.max(s)))
            _plt.xlabel("Key guesses")
            _plt.ylabel("Scores")
            _plt.title('Scores chart results byte '+str(key_byte), size = figure_axes_text_size)            

            # Plot convergence traces
            _plt.subplot(1,3,3)    
            for i in range(guesses_number): _plt.plot(self.attack_object_convergence_traces[i,key_byte,:].T, color = color_all_guesses)
            _plt.plot(self.attack_object_convergence_traces[best_guesses[key_byte],key_byte,:].T, color = color_best_guess, label = 'best score')
            if correct_key is not None:  
                _plt.plot(self.attack_object_convergence_traces[correct_key[key_byte],key_byte].T[:-1:DOWNS_STEP], color = color_right_guess, label = 'right key')
            # Set axes and legend
            _plt.xlabel('traces number', size = figure_axes_text_size)
            _plt.ylabel('score', size = figure_axes_text_size)
            _plt.xticks(_np.arange(0,CONV_POINTS, 1),_np.arange(1,CONV_POINTS+1, 1)*(self.attack_object_convergence_step), size = figure_axes_text_size)
            _plt.title('Convergence traces results byte '+str(key_byte), size = figure_axes_text_size)
            _plt.yticks(size = figure_axes_text_size)

            if do_not_save_figure_bool is False:                
                if self.figure_name_path is not None: 
                    path = self.figure_name_path+'results_byte_'+str(key_byte)
                    _plt.savefig(path)
            else:
                _plt.show()       

        else:      
            for i in range(guesses_number): _plt.plot(self.attack_object_results[i,key_byte].T[:-1:DOWNS_STEP], color = color_all_guesses)
            _plt.plot(self.attack_object_results[best_guesses[key_byte],key_byte].T[:-1:DOWNS_STEP], color = color_best_guess, label='best score')
            if correct_key is not None: 
                _plt.plot(self.attack_object_results[correct_key[key_byte],key_byte].T[:-1:DOWNS_STEP], color = color_right_guess, label='right key')
            # Set axes and legend
            _plt.xticks(size = figure_axes_text_size)
            _plt.xlabel('time', size = figure_axes_text_size)
            _plt.yticks(size = figure_axes_text_size)
            _plt.ylabel('score', size = figure_axes_text_size)
            _plt.title('Attack traces results', size = figure_axes_text_size)
            _plt.legend(loc="best")

        if do_not_save_figure_bool is False:                
            if self.figure_name_path is not None: 
                path = self.figure_name_path+'results_byte_'+str(key_byte)
                _plt.savefig(path)
        else:
            _plt.show()           

        print("Best guess for byte "+str(key_byte)+" = " + hex(best_guesses[key_byte]))
        if correct_key is not None:     
            print("Correct guess for byte : "+str(key_byte)+"=" + hex(correct_key[key_byte]))

            
    def plot_all_bytes(self, correct_key, do_not_save_figure_bool):
        DOWNS_STEP = 1
        guesses_number = self.attack_object_results.shape[0]
        best_guesses = self.attack_object_scores.argmax(0).squeeze()
        nb_bytes = self.attack_object_results.shape[1]
        
        ### --- If there is convergence results
        if self.attack_object_convergence_step is not None:
            CONV_POINTS =  self.attack_object_convergence_traces.shape[2]

            for key_byte in range(nb_bytes):            

                # Plot result traces
                _plt.subplot(nb_bytes,3,1+3*key_byte)
                for i in range(guesses_number): _plt.plot(self.attack_object_results[i,key_byte].T[:-1:DOWNS_STEP], color = color_all_guesses)
                _plt.plot(self.attack_object_results[best_guesses[key_byte],key_byte].T[:-1:DOWNS_STEP], color = color_best_guess, label='best score')
                if correct_key is not None: 
                    _plt.plot(self.attack_object_results[correct_key[key_byte],key_byte].T[:-1:DOWNS_STEP], color = color_right_guess, label='right key')
                # Set axes and legend
                _plt.xticks(size = figure_axes_text_size)
                _plt.xlabel('time', size = figure_axes_text_size)
                _plt.yticks(size = figure_axes_text_size)
                _plt.ylabel('score', size = figure_axes_text_size)
                _plt.title('Attack traces results byte '+str(key_byte), size = figure_axes_text_size)
                _plt.legend(loc="best")

                #plot results in bar chart
                _plt.subplot(nb_bytes,3,2+3*key_byte)        
                s = self.attack_object_scores[:, key_byte]
                _plt.bar(range(len(s)),s, color=color_all_guesses)
                _plt.bar(best_guesses[key_byte], s[best_guesses[key_byte]], color=color_best_guess) 
                if correct_key is not None:  
                    _plt.bar(correct_key[key_byte], s[correct_key[key_byte]], color=color_right_guess) 
                _plt.ylim((_np.min(s), _np.max(s)))
                _plt.xlabel("Key guesses")
                _plt.ylabel("Scores")
                _plt.title('Scores chart results byte '+str(key_byte), size = figure_axes_text_size)            

                # Plot convergence traces
                _plt.subplot(nb_bytes,3,3+3*key_byte)    
                for i in range(guesses_number): _plt.plot(self.attack_object_convergence_traces[i,key_byte,:].T, color = color_all_guesses)
                _plt.plot(self.attack_object_convergence_traces[best_guesses[key_byte],key_byte,:].T, color = color_best_guess, label = 'best score')
                if correct_key is not None:  
                    _plt.plot(self.attack_object_convergence_traces[correct_key[key_byte],key_byte].T[:-1:DOWNS_STEP], color = color_right_guess, label = 'right key')
                # Set axes and legend
                _plt.xlabel('traces number', size = figure_axes_text_size)
                _plt.ylabel('score', size = figure_axes_text_size)
                _plt.xticks(_np.arange(0,CONV_POINTS, 1),_np.arange(1,CONV_POINTS+1, 1)*(self.attack_object_convergence_step), size = figure_axes_text_size)
                _plt.title('Convergence traces results byte '+str(key_byte), size = figure_axes_text_size)
                _plt.yticks(size = figure_axes_text_size)

            if do_not_save_figure_bool is False:                
                if self.figure_name_path is not None: 
                    path = self.figure_name_path+'results_all_bytes'
                    _plt.savefig(path)
            else:
                _plt.show()       

        ### ----- If no convergence
        else:      
            for key_byte in range(self.attack_object_results.shape[1]):            
                _plt.subplot(nb_bytes,2,1+2*key_byte)        
                for i in range(guesses_number): _plt.plot(self.attack_object_results[i,key_byte].T[:-1:DOWNS_STEP], color = color_all_guesses)
                _plt.plot(self.attack_object_results[best_guesses[key_byte],key_byte].T[:-1:DOWNS_STEP], color = color_best_guess, label='best score')
                if correct_key is not None: 
                    _plt.plot(self.attack_object_results[correct_key[key_byte],key_byte].T[:-1:DOWNS_STEP], color = color_right_guess, label='right key')
                # Set axes and legend
                _plt.xticks(size = figure_axes_text_size)
                _plt.xlabel('time', size = figure_axes_text_size)
                _plt.yticks(size = figure_axes_text_size)
                _plt.ylabel('score', size = figure_axes_text_size)
                _plt.title('Attack traces results', size = figure_axes_text_size)
                _plt.legend(loc="best")

                #plot results in bar chart
                _plt.subplot(nb_bytes,2,2+2*key_byte)        
                s = self.attack_object_scores[:, key_byte]
                _plt.bar(range(len(s)),s, color=color_all_guesses)
                _plt.bar(best_guesses[key_byte], s[best_guesses[key_byte]], color=color_best_guess) 
                if correct_key is not None:  
                    _plt.bar(correct_key[key_byte], s[correct_key[key_byte]], color=color_right_guess) 
                _plt.ylim((_np.min(s), _np.max(s)))
                _plt.xlabel("Key guesses")
                _plt.ylabel("Scores")
                _plt.title('Scores chart results byte '+str(key_byte), size = figure_axes_text_size)            
                
                print("Best guess for byte "+str(key_byte)+" = " + hex(best_guesses[key_byte]))
                if correct_key is not None:     
                    print("Correct guess for byte : "+str(key_byte)+"=" + hex(correct_key[key_byte]))

            if do_not_save_figure_bool is False:                
                if self.figure_name_path is not None: 
                    path = self.figure_name_path+'results_all_bytes'
                    _plt.savefig(path)
            else:
                _plt.show()       

    def plot(self, key_byte=None, correct_key=None, do_not_save_figure_bool = False):
        """
        This function plot the distinguishers results.

        - parameters:
            - key_byte: give a selected key byte number, else None will plot all the bytes
            - correct_key: the right key if you know it, else it will only highlight the best scores
            - do_not_save_figure_bool: in case you have provided in the object a figure_name_path, by default = False so it will save the figures of the plot, else select False to not save the figures.
        """
        
        if key_byte is not None: 
            _plt.rcParams["figure.figsize"] = [22, 4]
            self._plot_single_byte(key_byte, correct_key, do_not_save_figure_bool)
        else:
            _plt.rcParams["figure.figsize"] = [14, 5*self.attack_object_results.shape[1]]
            self.plot_all_bytes(correct_key, do_not_save_figure_bool)
            
    def save(self, dist=True, conv=True, scores=True):
        """save the attack result in npz, npy files.

        Args:
            dist: default to true, save dist traces results in path given in object definition, if set to False no save
            conv: default to true, save dist conv traces in path given in object definition, if set to False no save
            scores: default to true, save dist score values in path given in object definition, if set to False no save     
        """        
        if self.file_name_path is not None:         
            if dist is True:
                path_dist = self.file_name_path+'dist_results'
                _np.savez(path_dist, self.attack_object_results)

            if self.attack_object_convergence_step is not None:
                if conv is True:
                    path_dist = self.file_name_path+'dist_conv'
                    _np.savez(path_dist, self.attack_object_convergence_traces)

            if scores is True:
                path_dist = self.file_name_path+'dist_scores'
                _np.savez(path_dist, self.attack_object_scores)
        else:
            print('No path defined for results storage')
           

    def print_best_scores(self, scores_number: int) -> None:
        """Display the best scores, in a notebook context.

        Args:
            scores_number: The number of scores to display.
        """

        bytes_number = self.attack_object_scores.shape[1]   
        num_A_scores = _np.nan_to_num(self.attack_object_scores)

        _display.display(_display.Markdown('__Best ' + str(scores_number)  + ' guesses for all key bytes__\n'))

        lines = []
        lines.append("Bytes")
        lines.append("------")
        lines.append("guess/score ")

        for byte_pos in range(bytes_number):
            best_scores = _np.flip(_np.argsort(num_A_scores[:, byte_pos], axis=0)[-scores_number:])

            lines[0] += "|" + str(byte_pos)
            lines[1] += "|--"

            for k in range(scores_number):        
                lines.append("guess/score ")
                lines[k+2] += "|("+str(hex(best_scores[k]))+f', {num_A_scores[best_scores[k], byte_pos]:.3f})'

        lines_display = lines[0] + "\n" + lines[1] + "\n"
        for i in range(scores_number):
            lines_display += lines[i+2] + "\n"

        _display.display(_display.Markdown(lines_display))     

    def print_scores(self, correct_key=None):
        """Display the best score per byte, in a notebook context.

        Args:
            correct_key: if provided gives the rank of each correct key byte.
        """

        bytes_number = self.attack_object_scores.shape[1]   
        num_A_scores = _np.nan_to_num(self.attack_object_scores)

        _display.display(_display.Markdown('__Best guesses for all key bytes__\n'))

        lines = []
        lines.append("Bytes")
        lines.append("------")
        lines.append("guess ")
        lines.append("score ")
        lines.append("right key ")
        lines.append("rank ")

        for byte_pos in range(bytes_number):
            best_scores = _np.flip(_np.argsort(num_A_scores[:, byte_pos], axis=0)[-1:])
            lines[0] += "|" + str(byte_pos)
            lines[1] += "|--"
            lines[2] += "|"+hex(best_scores[0])
            lines[3] += f'|{num_A_scores[best_scores[0], byte_pos]:.5f}'
            if correct_key is not None: 
                lines[4] += "|"+hex(correct_key[byte_pos])
                rank_right_key = _np.where(_np.flip(_np.argsort(num_A_scores[:, byte_pos], axis=0)) == correct_key[byte_pos])[0][0]+1
                lines[5] += "|"+str(rank_right_key)

        if correct_key is not None: 
            lines_display = lines[0] + "\n" + lines[1] + "\n" + lines[2] + "\n" + lines[3] + "\n" + lines[4] + "\n" + lines[5]
        else:
            lines_display = lines[0] + "\n" + lines[1] + "\n" + lines[2] + "\n" + lines[3]
        _display.display(_display.Markdown(lines_display))     
    
    def plot_attack_ranks(self, correct_key=None):

        if correct_key is not None: 
            _plt.rcParams['figure.figsize']=(17,5)

            bytes_number = self.attack_object_scores.shape[1] 
            rank_list = _np.zeros((bytes_number,self.attack_object_convergence_traces.shape[2]) ,dtype=_np.uint16)

            for step in range(self.attack_object_convergence_traces.shape[2]):
                num_A_scores = _np.nan_to_num(self.attack_object_convergence_traces[:,:,step])

                for byte_pos in range(bytes_number):
                    rank_right_key = _np.where(_np.flip(_np.argsort(num_A_scores[:, byte_pos], axis=0)) == correct_key[byte_pos])[0][0]+1
                    rank_list[byte_pos][step] = rank_right_key

            CONV_POINTS =  self.attack_object_convergence_traces.shape[2]
            for i in range(bytes_number):
                _plt.plot(rank_list[i].T, label="byte %d " %i)
            _plt.legend(prop={'size': graph_title_fontsize}, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)      
            _plt.title('Bytes rank evolution', size=graph_title_fontsize)
            _plt.xlabel('traces number')
            _plt.xticks(_np.arange(0,CONV_POINTS, 1),_np.arange(1,CONV_POINTS+1, 1)*(self.attack_object_convergence_step), size = graph_title_fontsize)
            _plt.show()    
        else:
            print('correct key unknown')
            

    def remaining_entropy_naive(self, correct_key, do_not_save_figure_bool=False):
        """Display the remaining entropy for the cases: best, worse and their mean.

        Args:
            -correct key: need the knowledge of the correct key
            - do_not_save_figure_bool: in case you have provided in the object a figure_name_path, by default = False so it will save the figures of the plot, else select False to not save the figures.           
        """
        
        if self.attack_object_convergence_step is None:
            print('No convergence result available')
            return [[], []]

        _plt.rcParams["figure.figsize"] = [20, 6]
        axes = _plt.gca()

        bytes_number = self.attack_object_scores.shape[1]   
        guesses_number = self.attack_object_results.shape[0]
        maxLog = bytes_number*_math.log2(guesses_number)
        entropy_min_list = [maxLog]
        entropy_max_list = [maxLog]

        for step in range(self.attack_object_convergence_traces.shape[2]):
            num_A_scores = _np.nan_to_num(self.attack_object_convergence_traces[:,:,step])
            rank_list = _np.zeros(bytes_number,dtype=_np.uint16)

            entropy_min = 0
            for byte_pos in range(bytes_number):
                best_scores = _np.flip(_np.argsort(num_A_scores[:, byte_pos], axis=0)[-1:])
                rank_right_key = _np.where(_np.flip(_np.argsort(num_A_scores[:, byte_pos], axis=0)) == correct_key[byte_pos])[0][0]+1
                rank_list[byte_pos] = rank_right_key
                entropy_min = entropy_min + _math.log2(rank_right_key)

            entropy_max = _math.log2(_np.max(rank_list))*bytes_number

            entropy_min_list.append(entropy_min)
            entropy_max_list.append(entropy_max)

        entropy_mean_list = _np.mean([_np.array(entropy_min_list), _np.array(entropy_max_list)], axis = 0)

        x1 = _np.arange(0, self.attack_object_processed_traces, self.attack_object_convergence_step)
        x1 = _np.hstack((x1,self.attack_object_processed_traces))
        y1 = _np.array(entropy_min_list)
        x2 = x1
        y2 = _np.array(entropy_max_list)
        y3 = entropy_mean_list

        line_32 = _np.tile(32, len(x1))
        # Get abcisse when entropy is lower to 32 bits
        idx_mean = _np.argwhere((entropy_mean_list-line_32)<0).flatten()    
        if (len(idx_mean) != 0):
            traces_mean = x1[idx_mean[0]]
        else:
            traces_mean = None

        idx_min = _np.argwhere((entropy_min_list-line_32)<0).flatten()    
        if (len(idx_min) != 0):
            traces_min = x1[idx_min[0]]
        else:
            traces_min = None

        idx_max = _np.argwhere((entropy_max_list-line_32)<0).flatten()    
        if (len(idx_max) != 0):
            traces_max = x1[idx_max[0]]
        else:
            traces_max = None    

        if 0 in entropy_mean_list:
            line_0 = _np.tile(0, len(x1))
            idx_success = _np.argwhere((entropy_max_list-line_0)==0).flatten()[0]
            traces_success = x1[idx_success]
        else:
            traces_success = None      

        axes.set_xlabel('Number of traces')
        axes.set_ylabel('Key remaining entropy, log2')
        _plt.plot(x1, y1, color = 'green', label='best entropy')
        _plt.plot(x1, y2, color = 'black', label='worse entropy')
        _plt.plot(x1, y3, color = 'red', label='mean entropy')    
        _plt.plot(x1, line_32, '--', color = 'black', label='2^32')    
        _plt.xlim(0)    
        _plt.ylim(0)
        _plt.legend()
        _plt.title('Guessing Entropy Graph', fontsize = 14)

        _plt.fill(
            _np.append(x1, x2[::-1]),
            _np.append(y1, y2[::-1]),
        )  
        
            
        if do_not_save_figure_bool is False:                
            if self.figure_name_path is not None: 
                path = self.figure_name_path+'remaining_entropy_naive'
                _plt.savefig(path)
        else:
            _plt.show()       
            
        print('-----------------------------------------------------------')    
        print('Number of traces for full key recovery            = ',traces_success)
        print('-----------------------------------------------------------')    
        print('Number of traces for 32-bit remaining max-entropy  = ',traces_max)
        print('Number of traces for 32-bit remaining min-entropy  = ',traces_min)
        print('Number of traces for 32-bit remaining mean-entropy = ',traces_mean)
        print('-----------------------------------------------------------')

        return entropy_min_list, entropy_max_list, entropy_mean_list

 
    """
    RankEstimation implements an algorithm proposed here https://eprint.iacr.org/2014/920.pdf
    It takes as an input an array p of probabilities for each engine and guess,
    the real key and a parameter binWidth, controling the accuracy of the estimation.
    It outputs the lower bound, estimated rank and upper bound
    :param p: probabilities of each guess and engines
    :param key_real: the real key
    :param binWidth: parameter controlling the accuracy
    :return: (lower bound, estimated rank, upper bound)

    """
    def RankEstimation(self,p, key_real, binWidth):

        q=_np.log(p)
        q=_np.nan_to_num(q,neginf=-100)# requires numpy version 1.17 or newer!!! but makes the algorithm more stable
        subkeyNum = p.shape[0]
        histMin = 0
        y = _np.array(1, dtype=_np.float64)
        #Convolve the histograms
        for subkeyNo in range(subkeyNum):
            maxi, mini = _np.max(q[subkeyNo]), _np.min(q[subkeyNo])
            bins = max(int(_np.ceil((maxi-mini)/binWidth)),1)
            maxi = mini + bins*binWidth #ensures equal binsize across histograms
            hist, edges = _np.histogram( q[subkeyNo], bins=bins, range=(mini,maxi))
            histMin = histMin + edges[0]
            y = _np.convolve(y, hist)
        #calculate bin number of the real key
        binNoReal = 0
        for subkeyNo in range(subkeyNum):
            candNo = key_real[subkeyNo]
            binNoReal = binNoReal + q[subkeyNo, candNo]
        binNoReal = int(( binNoReal - histMin ) / binWidth)

        binNoMax = max(0,binNoReal-subkeyNum)
        keyRankMax = _np.sum(y[binNoMax:])

        binNoMin = binNoReal+subkeyNum
        keyRankMin = _np.sum(y[binNoMin:])

        binNoEst = binNoReal
        keyRankEst = _np.sum(y[binNoEst:])

        return keyRankMin, keyRankEst, keyRankMax


    def remaining_entropy(self, correct_key, do_not_save_figure_bool=False):
        """Display the remaining entropy based on estimation method given in paper:
            - [GlowaczGPSS15] Cezary Glowacz, Vincent Grosso, Romain Poussier, Joachim Schüth, François-Xavier Standaert: Simpler and More Efficient Rank Estimation for Side-Channel Security Assessment. FSE 2015: 117-129

        Args:
            - correct key: need the knowledge of the correct key
            - do_not_save_figure_bool: in case you have provided in the object a figure_name_path, by default = False it will save the figures of the plot, else select False to not save the figures.           
        """

        if self.attack_object_convergence_step is None:
            print('No convergence result available')
            return [[], []]

        _plt.rcParams["figure.figsize"] = [20, 6]
        axes = _plt.gca()

        bytes_number = self.attack_object_scores.shape[1]   
        guesses_number = self.attack_object_results.shape[0]
        maxLog = bytes_number*_math.log2(guesses_number)
        key_rank_lower = [maxLog]
        key_rank_max = [maxLog]
        key_rank_est = [maxLog]

        for step in range(self.attack_object_convergence_traces.shape[2]):
            scores = _np.nan_to_num(self.attack_object_convergence_traces[:,:,step]).T
            scores.shape
            #in case that all scores have value 0 for an engine, add a constant,
            #so normalizaion won't fail
            for i in range(scores.shape[0]):
                if _np.all(scores[i]==0):
                    scores[i]+=1

            probabilities = _np.nan_to_num(scores/_np.expand_dims(scores.sum(1),1))

            rank_est = self.RankEstimation(probabilities, correct_key, 0.005)
    #        rank_est = RankEstimation(probabilities, correct_key, 0.02)


            key_rank_lower.append(_math.log2(rank_est[0]+1))
            key_rank_est.append(_math.log2(rank_est[1]+1))
            key_rank_max.append(_math.log2(rank_est[2]+1))

        # Plot all results
        x1 = _np.arange(0, self.attack_object_processed_traces, self.attack_object_convergence_step)
        x1 = _np.hstack((x1,self.attack_object_processed_traces))
        y1 = _np.array(key_rank_lower)
        x2 = x1
        y2 = _np.array(key_rank_max)
        y3 = key_rank_est

        line_32 = _np.tile(32, len(x1))
        # Get abcisse when entropy is lower to 32 bits
        idx_est = _np.argwhere((key_rank_est-line_32)<0).flatten()    
        if (len(idx_est) != 0):
            traces_est = x1[idx_est[0]]
        else:
            traces_est = None

        idx_lower = _np.argwhere((key_rank_lower-line_32)<0).flatten()    
        if (len(idx_lower) != 0):
            traces_lower = x1[idx_lower[0]]
        else:
            traces_lower = None

        idx_max = _np.argwhere((key_rank_max-line_32)<0).flatten()    
        if (len(idx_max) != 0):
            traces_max = x1[idx_max[0]]
        else:
            traces_max = None    

        if 0 in key_rank_est:
            line_0 = _np.tile(0, len(x1))
            idx_success = _np.argwhere((key_rank_est-line_0)==0).flatten()[0]
            traces_success = x1[idx_success]
        else:
            traces_success = None      

        axes.set_xlabel('Number of traces')
        axes.set_ylabel('Key remaining entropy, log2')
        _plt.plot(x1, line_32, '--', color = 'black', label='2^32')    
        _plt.plot(x1, y1, color = 'green', label='rank ge lower bound')
        _plt.plot(x1, y2, color = 'black', label='rank ge higher bound')
        _plt.plot(x1, y3, color = 'red', label='rank ge estimated entropy')    
        _plt.xlim(0)    
        _plt.ylim(0)
        _plt.legend()
        _plt.title('Guessing Entropy Graph', fontsize = 14)

        _plt.fill(
            _np.append(x1, x2[::-1]),
            _np.append(y1, y2[::-1]),
            color = 'lightgreen'
        )    

        print('-----------------------------------------------------------')    
        print('Number of traces for full key recovery            = ',traces_success)
        print('-----------------------------------------------------------')    
        print('Number of traces for 32-bit remaining entropy: ')
        print('-- Higher bound entropy  = ',traces_max)
        print('-- Lower bound entropy   = ',traces_lower)
        print('-- Estimated entropy     = ',traces_est)
        print('-----------------------------------------------------------')

        if do_not_save_figure_bool is False:                
            if self.figure_name_path is not None: 
                path = self.figure_name_path+'remaining_entropy'
                _plt.savefig(path)
        else:
            _plt.show()       
        
        return key_rank_lower, key_rank_est, key_rank_max


