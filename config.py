
prime_upperbound = 100
prime_lowerbound = 0


number_of_candidates = 4


number_of_bits = 2


minimum_n_value = int(''.join([''.join(["1" for y in range(0, number_of_bits)]) for x in range(0, number_of_candidates)]), 2) + 1  # 256


voter = 3