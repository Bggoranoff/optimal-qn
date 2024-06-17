compile:
	cmake . -B build
	$(MAKE) -C build/
	rm -f ./OptimalNearTerm
	ln -s build/OptimalNearTerm ./OptimalNearTerm

clean:
	rm -rf build
	rm -f OptimalNearTerm
