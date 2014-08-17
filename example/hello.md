# hello world

Print hello world

    $actually do it
    printf("Hello, world!");

Put a `main()` function around that printf call.

    $main
    int main(int argc, char **argv)
    {
        %actually do it
        return 0;
    }

Include stdio.h

    $_main
    #include <stdio.h>
    %main
