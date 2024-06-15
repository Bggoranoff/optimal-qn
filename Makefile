compile:
	cmake . -B build
	$(MAKE) -C build/
	ln -s build/OptimalNearTerm ./OptimalNearTerm

clean:
	rm -rf build
