import random
# random.seed(0)

class i_GWO():
    def __init__(self, iterations, pack_size, vector_size):
        self.iterations = iterations
        self.pack_size = pack_size
        self.vector_size = vector_size
        
    # generate wolf
    def wolf(self, vector_size, min_range, max_range):
      wolf_position = [0.0 for i in range(vector_size)]
      for i in range(vector_size):
        wolf_position[i] = ((max_range - min_range) * random.random() + min_range)
      return wolf_position
  
    # generate wolf pack
    def pack(self):
        pack = [self.wolf(self.vector_size, -10, 10) for i in range(self.pack_size)]
        return pack
    
    def fitness(self, individual):
        fitness = 0
        for i in individual:
            a = i ** 2
            fitness += a
        return fitness
    
    def hunt(self):
        # generate wolf pack
        wolf_pack = self.pack()
        # sort pack by fitness
        pack_fit = sorted([(self.fitness(i), i) for i in wolf_pack])
        
        # main loop
        for k in range(self.iterations):
            # select alpha, beta and delta
            alpha, beta, delta = pack_fit[0][1], pack_fit[1][1], pack_fit[2][1]
            
            print('iteration: {}, best_wolf_position: {}'.format(k,self.fitness(alpha)))
            
            # linearly decreased from 2 to 0
            a = 2*(1 - k/self.iterations)
            
            # updating each population member with the help of alpha, beta and delta
            for i in range(self.pack_size):
                # compute A and C 
                A1, A2, A3 = a * (2 * random.random() - 1), a * (2 * random.random() - 1), a * (2 * random.random() - 1)
                C1, C2, C3 = 2 * random.random(), 2*random.random(), 2*random.random()
                
                # generate vectors for new position
                X1 = [0.0 for i in range(self.vector_size)]
                X2 = [0.0 for i in range(self.vector_size)]
                X3 = [0.0 for i in range(self.vector_size)]
                X_GWO = [0.0 for i in range(self.vector_size)]
                
                # hunting 
                for j in range(self.vector_size):
                    X1[j] = alpha[j] - A1 * abs(C1 - alpha[j] - wolf_pack[i][j])
                    X2[j] = beta[j] - A2 * abs(C2 - beta[j] - wolf_pack[i][j])
                    X3[j] = delta[j] - A3 * abs(C3 - delta[j] - wolf_pack[i][j])
                    X_GWO[j] += X1[j] + X2[j] + X3[j]
                
                for j in range(self.vector_size):
                    X_GWO[j] /= 3.0

                # fitness calculation of new position candidate
                new_fitness = self.fitness(X_GWO)
                
                # current wolf fitness
                current_wolf = wolf_pack[i]
                
                # Begin i-GWO ehancement, Compute R --------------------------------
                R = self.fitness(current_wolf) - new_fitness
                
                # Compute eq. 11, build the neighborhood
                neighborhood = []
                for l in wolf_pack:
                    neighbor_distance = self.fitness(current_wolf) - self.fitness(l)
                    if neighbor_distance <= R:
                        neighborhood.append(l)
                        
                # if the neigborhood is empy, compute the distance with respect 
                # to the other wolfs in the population and choose the one closer
                closer_neighbors = []
                if len(neighborhood) == 0:
                    for n in wolf_pack:
                        distance_wolf_alone = self.fitness(current_wolf) - self.fitness(n)
                        closer_neighbors.append((distance_wolf_alone,n))
                        
                    closer_neighbors = sorted(closer_neighbors)
                    neighborhood.append(closer_neighbors[0][1])
                
                # Compute eq. 12 compute new candidate using neighborhood
                X_DLH = [0.0 for i in range(self.vector_size)]
                for m in range(self.vector_size):
                    random_neighbor = random.choice(neighborhood)
                    random_wolf_pop = random.choice(wolf_pack)
                    
                    X_DLH[m] = current_wolf[m] + random.random() * random_neighbor[m] - random_wolf_pop[m]
                
                # if X_GWO is better than X_DLH, select X_DLH
                if self.fitness(X_GWO) < self.fitness(X_DLH):
                    candidate = X_GWO
                else:
                    candidate = X_DLH
                    
                # if new position is better then replace, greedy update
                if self.fitness(candidate) < self.fitness(wolf_pack[i]):
                    wolf_pack[i] = candidate
         
            # sort the new positions by their fitness
            pack_fit = sorted([(self.fitness(i), i) for i in wolf_pack])
            
def main():
    model = i_GWO(iterations = 20,  pack_size = 10, vector_size = 3)
    model.hunt()

if __name__ == '__main__':
    main()
