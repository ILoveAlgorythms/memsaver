FROM gcc:latest
COPY a.cpp /
RUN g++ a.cpp -o a.exe
CMD ./a.exe \
/.a.exe
