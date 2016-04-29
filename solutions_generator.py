# collect all .out files into solutions.out
# and write a report of all results

if __name__ == "__main__":
	solutions_file = open('solutions.out', "w")
	report = open('report.txt', "w")

	for i in range(1, 493):
		out_file = open("phase1-processed/" + str(i)+ ".out", "r")
		first_line = out_file.readline()
		solutions_file.write(first_line + '\n')
		report.write(str(i)+".OUT\n")
		for line in out_file.readlines():
			report.write(line)
		report.write("\n")
	solutions_file.close()
	report.close()



