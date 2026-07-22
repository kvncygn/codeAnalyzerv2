// engine.cpp - C++ file: only file-level metrics, TCF=0 Helpers=0
#include <string>

/*
 * block comment
 * over multiple lines
 */
int compute(int a, int b) {
    std::string s = R"(raw string with // not a comment and /* not either)";
    int sum = a + b; // inline comment counts as code + comment + inline

    return sum;
}
