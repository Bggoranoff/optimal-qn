compile:
	cmake -DCMAKE_C_COMPILER=/opt/homebrew/opt/llvm@16/bin/clang . -B build
	$(MAKE) -C build/
	rm -f ./OptimalNearTerm
	ln -s build/OptimalNearTerm ./OptimalNearTerm

experiments: OptimalNearTerm
	rm -rf results
	mkdir results
	./OptimalNearTerm policyIter 2 0.5 "0.1, 0.2, 0.3, 0.4" 1.0 0.1 1e-20 ./results/output2.json
	./OptimalNearTerm policyIter 3 0.5 "0.1, 0.2, 0.3, 0.4" 1.0 0.1 1e-20 ./results/output3.json
	./OptimalNearTerm policyIter 4 0.5 "0.1, 0.2, 0.3, 0.4" 1.0 0.1 1e-20 ./results/output4.json
	./OptimalNearTerm policyIter 5 0.5 "0.1, 0.2, 0.3, 0.4" 1.0 0.1 1e-20 ./results/output5.json
	./OptimalNearTerm policyIter 6 0.5 "0.1, 0.2, 0.3, 0.4" 1.0 0.1 1e-20 ./results/output6.json
	./OptimalNearTerm policyIter 7 0.5 "0.1, 0.2, 0.3, 0.4" 1.0 0.1 1e-20 ./results/output7.json

clean:
	rm -rf build
	rm -f OptimalNearTerm
