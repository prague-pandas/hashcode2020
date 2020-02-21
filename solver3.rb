#!/usr/bin/ruby

ARGV[0] = "c_incunabula.txt"

file = {ARGV[0] => 0}

@shuffle_indexes = [0,0]

def writeFile file, ret, score
	File.open("out/#{file}_#{score}.a", "w") { |out|
		out.write "#{ret.size}\n"
		out.write ret.join("\n")
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

def shuffle(libs, size)
	@shuffle_indexes = [rand(size), rand(size)]
	do_swap(libs)
end

def do_swap(libs)
	bak = libs[@shuffle_indexes[0]]
	libs[@shuffle_indexes[0]] = libs[@shuffle_indexes[1]]
	libs[@shuffle_indexes[1]] = bak
	libs
end


numB, numL, numD = nil
bookScore = []

File.open("input/#{file.keys.first}", "r") { |input| 
	rows = input.read.split("\n")

	numB, numL, numD = rows.shift.split(" ").map &:to_i
	bookScore_orig = rows.shift.split(" ").map &:to_i

	id = 0
	libs = []

	while rows.size > 0
		libs << [id, rows.shift.split(" ").map(&:to_i), rows.shift.split(" ").map(&:to_i)]
		id += 1
	end

	while true do

		@finalScore = 0
		bookScore = bookScore_orig.dup
		daysLeft = numD

		ret = []

		shuffle(libs, numL).each do |lib|
			took, books = processLib(lib[1], lib[2], daysLeft, bookScore)
			daysLeft -= took

			ret << [[lib[0], books.size].join(" "), books.join(" ")] if books.size > 0

			id += 1
		end

		if @finalScore > file[file.keys.first]
			writeFile(file.keys.first, ret, @finalScore)

			file[file.keys.first] = @finalScore
			puts "#{@finalScore}: #{file}"
			$stdout.flush
		else
			do_swap(libs)
		end
	end
 }