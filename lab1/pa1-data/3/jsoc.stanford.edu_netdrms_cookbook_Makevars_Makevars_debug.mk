makevars_debug mk same as makevars_linux_x86_64 mk with debug flags revision history is at the end of the file to make full use of these variable definitions setting debug symbols you should first build a debug version of the drms libraries by running at the drms root setenv jsoc_debug 1 make mach debug make make usr bin make the shell this must be a valid shell eg sh or csh or tcsh echo also works as a no op shell bin sh commands and arguments ar archive ranlib ar usr bin ar arflags crv ranlib usr bin ranlib as assembler as usr bin as asflags cc c compiler ncc usr bin cc gcc usr bin gcc icc usr local bin icc mcmodel medium cc icc cdebug g cdefines dbeta cflags o3 std c99 d_file_offset_bits 64 xw d_gnu_source cflags std c99 xw d_gnu_source ccflags c cflags ccflags c g std c99 d_file_offset_bits 64 xw d_gnu_source cincludes i jsoc base include i usr include dbcc cc cdebug fw fullwarn multi hfiles cfiles f77 fortran fc usr bin f77 fc usr local bin ifort fflags o c flibs lcm lftn lf77 lm lu77 li77 lblas lisam lm ld link editor ld usr bin ld ldflags xw openmp ldcmd cc ldflags malchk loadlibes parlibs objs aout noaout aouts noaouts lex lexical analyser lex usr bin lex lflags yacc yacc usr bin yacc yflags oracle for platform oracle_home oraadd rpc rpclib miscellaneous commands awk bin awk cd cd chgrp bin chgrp chmod bin chmod chown bin chown cp bin cp cpp usr bin cpp date bin date echo echo install usr bin install ln bin ln ls bin ls mkdir bin mkdir mv bin mv rm bin rm f strip usr bin strip touch bin touch xstr echo revision history 07.04 19 created this file based on rick genmake d makevars_linux4 mk 07.05 29 modified to support jsoc module builds
