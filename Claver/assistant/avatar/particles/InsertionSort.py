class InsertionSort:

    @staticmethod
    def sortHighToLow(list):
        for i in range(len(list)):
            particle = list[i]
            if particle.getDistance() > list[i - 1].getDistance():
                InsertionSort.sortUpHighToLow(list, i)

    @staticmethod
    def sortUpHighToLow(list, i):
        particle = list[i]
        attemptPos = i - 1
        while attemptPos != 0 and (list[attemptPos - 1].getDistance() < particle.getDistance()):
            attemptPos -= 1
        list.remove(i)
        list.insert(attemptPos, particle)
