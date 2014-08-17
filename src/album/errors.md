# Errors

`LPError` is the base class for all `album` user errors.

    $lperror
    class LPError(Exception):
        pass

We define subclasses for syntax and semantics errors.

    $error subclasses
    class LPSyntaxError(Exception):
        pass


    class LPSemanticError(Exception):
        pass

-

    $_main
    %lperror
    %error subclasses
