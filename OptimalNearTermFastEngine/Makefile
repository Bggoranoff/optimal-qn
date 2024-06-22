compile:
	cmake -DCMAKE_C_COMPILER=/opt/homebrew/opt/llvm@16/bin/clang . -B build
	$(MAKE) -C build/
	rm -f ./OptimalNearTerm
	ln -s build/OptimalNearTerm ./OptimalNearTerm

clean:
	rm -rf build
	rm -f OptimalNearTerm
