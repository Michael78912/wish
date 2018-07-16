#### The scripting branch

Hi! if you are actually reading this thing, I congratulate you.
anyway, I have just started working on the scripting, and here is
kind of what i want (in order)

1. To have the scripts _actually work_
2. be able to declare subroutines
3. conditional tests (AKA `if`)
4. looping (`while`/`for`/`foreach`) (who needs `until`???)
5. type definitions (telling it that `a` is a number, etc...)
6. _maybe_ functions. (if i feel like doing a ton of work)
7. who knows

an example of a very roundabout script is below:

    # this program prints hello 3 times, in a much more complex way than it needs to be.
    SUBROUTINE say: $arg $amount  # declare "hi" with 2 parameters
      amount->int  # tell it that amount is an integer
      FOR $i=0 $i<$amount $i++  # for loop
        echo $i  # actually echo it
      END FOR  # end the for loop
    END SUBROUTINE say  # end the subroutine

    SUBROUTINE main  # main sub
      say: Hello 3  # call say with Hello and 3
    END SUBROUTINE main

    main:

as you can probably tell, "#" is a comment.  
it will not be case-sensitive, as practically nothing about windows is, (environment variables, 
file names, etc...) so (in my opinion) it makes sense to have keywords be too. indentation wont matter,
but is there too look nice. `:` is required to call a subroutine, with parameters behind, seperated by 
whitespace. **_ALL VARIABLES_** must be prefixed by `$`, including parameters. as with normal commands, 
to pass a parameter with spaces/tabs/any whitespace, use quotes.
