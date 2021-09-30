import math
from datetime import datetime, timedelta
# pickup lat pickup long dropoff lat drop off long
import map

def get_fitness(chromosome, fit):
    tot_distances = 0
    tot_time = 0
    for g in range(len(chromosome) - 1):
        loc1 = str(chromosome[g][4]) + "," + str(chromosome[g][5])
        loc2 = str(chromosome[g + 1][2]) + "," + str(chromosome[g + 1][3])

        trip_time = int(chromosome[g][7]) / 60
        tot_time += trip_time
        trip_distance = int(chromosome[g][6]) / 1000
        tot_distances += trip_distance

        time_distance = map.timeDistance(loc1, loc2)
        driving_time_between = time_distance[0]
        tot_time += driving_time_between
        distance_between = time_distance[1]
        tot_distances += distance_between

        trip1_start_time = datetime(year=1, month=1, day=1, hour=(int(chromosome[g][1].split(":")[0])),
                                    minute=(int(chromosome[g][1].split(":")[1])))
        trip2_start_time = datetime(year=1, month=1, day=1, hour=(int(chromosome[g + 1][1].split(":")[0])),
                                    minute=(int(chromosome[g + 1][1].split(":")[1])))
        time_between = trip2_start_time - trip1_start_time
        extra_time = time_between - timedelta(minutes=tot_time)
        if fit:
            print()
            print("gene 1:", chromosome[g])
            print("gene 2:", chromosome[g + 1])
            print("t1", trip1_start_time)
            print("t2", trip2_start_time)
            print("time between", time_between)
            print("driving mins", tot_time)
            print("extra time", extra_time)
            print()
        # time_between_mins = int(time_between.strftime("%H:%M:%S").split(":")[0]*60 + int(time_between.strftime("%H:%M:%S").split(":")[1]))
        # extra_time = time_between_mins - (tot_time/60)

        # TODO add trip between times and requested times (subtract driving time from requested time differences and add that to driving times)


def find_mates(gene, parents, mates):
    # this will be run with a one dimensional array & never null time
    #  remember, you're looping through half the population (105)
    possible_mates = []
    previous_start_time = datetime(year=1, month=1, day=1, hour=(int(gene[1].split(":")[0])),
                                   minute=(int(gene[1].split(":")[1])))
    duration = int(gene[7])

    if mates:
        print("mate 1:", gene)
        print("mate 1 start time:", previous_start_time.strftime("%H:%M:%S"))
        print()

    for g in range(len(parents)):
        loc1 = str(gene[4]) + "," + str(gene[5])
        loc2 = str(parents[g][2]) + "," + str(parents[g][3])
        trip_time = int(gene[7]) / 60
        tot_time = trip_time

        #time_distance = googlemaps.timeDistance(loc1, loc2)
        #driving_time_between = time_distance[0]
        driving_time_between = 20
        tot_time += driving_time_between

        window = tot_time
        tot_time = previous_start_time + timedelta(seconds=duration + window)


        next_start_time = datetime(year=1, month=1, day=1, hour=(int(parents[g][1].split(":")[0])),
                                   minute=(int(parents[g][1].split(":")[1])))
        if mates:
            print("possible mate 2:", parents[g])
            print("start_time", next_start_time.strftime("%H:%M:%S"))
            print("driving time:", window, "minutes")

        if next_start_time >= tot_time:
            possible_mates.append(parents[g])

            if mates:
                print(next_start_time.strftime("%H:%M:%S"), ">", tot_time.strftime("%H:%M:%S"))
                print("can complete trip in time")
                print()
        else:
            if mates:
                print(next_start_time.strftime("%H:%M:%S"), "<", tot_time.strftime("%H:%M:%S"))
                print("cannot complete trip in time")
                print()

    for i in range(len(possible_mates)):
        for j in range(0, len(possible_mates) - i - 1):
            # Swap if current element is greater than next
            current_time = int(possible_mates[j][1].split(":")[0] + possible_mates[j][1].split(":")[1])
            next_time = int(possible_mates[j + 1][1].split(":")[0] + possible_mates[j + 1][1].split(":")[1])
            if current_time > next_time:
                possible_mates[j], possible_mates[j + 1] = possible_mates[j + 1], possible_mates[j]

    return possible_mates


def crossover(parents, cross):
    #offspring = ["ID", "RequestedPickUpTime","PickUpLat","PickUpLng","DropOffLat","DropOffLng",	"EstimatedDistance","EstimatedDuration (s)","SeatingNeedCode"]
    offspring = []
    remove_genes = []
    drivers = 25  # 25 = num of drivers

    for c in range(drivers):
        chromosome = []

        parents = get_updated_parents(remove_genes, parents)
        for i in range(len(parents)):
            for j in range(0, len(parents) - i - 1):
                # Swap if current element is greater than next
                current_time = int(parents[j][1].split(":")[0] + parents[j][1].split(":")[1])
                next_time = int(parents[j + 1][1].split(":")[0] + parents[j + 1][1].split(":")[1])
                if current_time > next_time:
                    parents[j], parents[j + 1] = parents[j + 1], parents[j]

        gene1 = parents[0]
        chromosome.append(gene1)
        remove_genes.append(gene1)
        offspring.append(chromosome)

    if cross:
        print("FIRST PASS")
        for i in range(len(offspring)):
            print(offspring[i])

    for c2 in range(drivers):
        # if cross:
        # print("possible mates: ", len(find_mates(offspring[c2][0], get_updated_parents(remove_genes, parents), mates=False)))
        if len(find_mates(offspring[c2][0], get_updated_parents(remove_genes, parents), mates=False)) > 0:
            gene2 = find_mates(offspring[c2][0], get_updated_parents(remove_genes, parents), mates=False)[0]
            remove_genes.append(gene2)
            offspring[c2].append(gene2)

    if cross:
        print()
        print("SECOND PASS")
        for j in range(len(offspring)):
            print(offspring[j])

    for c3 in range(drivers):
        # if cross:
        # print("possible mates: ", len(find_mates(offspring[c3][0], get_updated_parents(remove_genes, parents), mates=False)))
        if len(offspring[c3]) == 2:
            if len(find_mates(offspring[c3][1], get_updated_parents(remove_genes, parents), mates=False)) > 0:
                gene3 = find_mates(offspring[c3][1], get_updated_parents(remove_genes, parents), mates=False)[0]
                remove_genes.append(gene3)
                offspring[c3].append(gene3)
        else:
            if len(find_mates(offspring[c3][0], get_updated_parents(remove_genes, parents), mates=False)) > 0:
                gene3 = find_mates(offspring[c3][0], get_updated_parents(remove_genes, parents), mates=False)[0]
                remove_genes.append(gene3)
                offspring[c3].append(gene3)

    if cross:
        print()
        print("THIRD PASS")
        for j in range(len(offspring)):
            print(offspring[j])
        print("genes left:", len(get_updated_parents(remove_genes, parents)))

    for c4 in range(drivers):

        if len(offspring[c4]) == 3:
            if len(find_mates(offspring[c4][2], get_updated_parents(remove_genes, parents), mates=False)) > 0:
                gene4 = find_mates(offspring[c4][2], get_updated_parents(remove_genes, parents), mates=False)[0]
                remove_genes.append(gene4)
                offspring[c4].append(gene4)

        elif len(offspring[c4]) == 2:
            if len(find_mates(offspring[c4][1], get_updated_parents(remove_genes, parents), mates=False)) > 0:
                gene4 = find_mates(offspring[c4][1], get_updated_parents(remove_genes, parents), mates=False)[0]
                remove_genes.append(gene4)
                offspring[c4].append(gene4)

        else:
            if len(find_mates(offspring[c4][0], get_updated_parents(remove_genes, parents), mates=False)) > 0:
                gene4 = find_mates(offspring[c4][0], get_updated_parents(remove_genes, parents), mates=False)[0]
                remove_genes.append(gene4)
                offspring[c4].append(gene4)

    if cross:
        print()
        print("FOURTH PASS")
        for j in range(len(offspring)):
            print(offspring[j])

        print("genes left:", len(get_updated_parents(remove_genes, parents)))
    return offspring


def get_updated_parents(remove_genes, parents):
    temp_parents = []
    for c in range(len(parents)):
        temp_parents.append(parents[c])
    updated = [elem for elem in temp_parents if elem not in remove_genes]
    return updated
