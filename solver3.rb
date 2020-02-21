#!/usr/bin/ruby

file_name = ARGV[0] ||= "c_incunabula.txt"

@starting_score = 0

@startedAt = Time.now.to_i

@shuffle_indexes = [0,0]

def writeFile file, ret, score, libs
	libs = libs.map{|l| l[0]}.join(" ")

	File.open("out/#{file}_#{score}.a", "w") { |out|
		out.write "#{ret.size}\n"
		out.write ret.inject(""){|m,l| m + "#{l[0]} #{l[1]}\n#{l[2].join(" ")}\n"}
	}
	File.open("out/_best_#{file}.0", "w") { |out|
		out.write "#{score}\n"
		out.write libs
	}
	File.open("out/_best_#{file}.#{@startedAt}", "w") { |out|
		out.write "#{score}\n"
		out.write libs
	}
end


def processBooks books, max, scores
	books.map do |book|
		[book, scores[book]]
	end.sort_by!{|e| e[1]}.reverse[0..max-1].inject([]) do |sum, e|
		if e[1] > 0
			scores[e[0]] = 0
			@finalScore += e[1]
			sum << e[0]
		else
			return sum
		end
	end
end

def processLib head, books, daysLeft, scores
	numOfBooks, signUp, perDay = head

	return [signUp, []] if signUp >= daysLeft

	processedBooks = processBooks(books, (daysLeft-signUp)*perDay, scores)

	[signUp, processedBooks]
end

def shuffle(libs, size, low_index)
	(((x=rand(size))+1) / (rand(x)+1)).round.times {
		@shuffle_indexes = [rand(low_index), rand(size)]
		do_swap(libs)
	}
	libs
end

def do_swap(libs)
	bak = libs[@shuffle_indexes[0]]
	libs[@shuffle_indexes[0]] = libs[@shuffle_indexes[1]]
	libs[@shuffle_indexes[1]] = bak
	libs
end

def initSort(libs, file)
	sorted_libs = []

	File.open("out/_best_#{file}.0", "r") { |input|
		rows = input.read.split("\n")
		@starting_score = rows.shift.to_i

		indexes = rows.shift.split(" ").map &:to_i

		indexes.each_with_index do |target_index, index|
			sorted_libs[index] = libs[target_index]
		end
	} rescue return libs.shuffle

	sorted_libs
end


numB, numL, numD = nil
bookScore = []

File.open("input/#{file_name}", "r") { |input| 
	rows = input.read.split("\n")

	numB, numL, numD = rows.shift.split(" ").map &:to_i
	bookScore_orig = rows.shift.split(" ").map &:to_i

	shuffle_low_index = [numL, numD].min

	id = 0
	libs = []

	while rows.size > 0
		libs << [id, rows.shift.split(" ").map(&:to_i), rows.shift.split(" ").map(&:to_i)]
		id += 1
	end

	libs_best = initSort(libs, file_name)

	while true do

		@finalScore = 0
		bookScore = bookScore_orig.dup
		libs = libs_best.dup
		daysLeft = numD

		ret = []

		shuffle(libs, numL, shuffle_low_index).each do |lib|
			took, books = processLib(lib[1], lib[2], daysLeft, bookScore)
			daysLeft -= took

			ret << [lib[0], books.size, books] if books.size > 0

			break if daysLeft <= 0

			id += 1
		end

		if @finalScore > @starting_score
			writeFile(file_name, ret, @finalScore, libs)

			@starting_score = @finalScore

			libs_best = libs

			puts "#{@finalScore}: #{file_name}"
			$stdout.flush
		end
	end
 }