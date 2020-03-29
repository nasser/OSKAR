// Learn more about F# at http://fsharp.org

open System
open System.Diagnostics
open Generated
open System.IO

let test s =
    let sw = Stopwatch.StartNew()
    let tree = parse s
    let t = sw.ElapsedMilliseconds
    match tree with
    | Some tree -> printfn "%A\n%A\n%dms\n\n" s tree t
    | None -> printfn "%A\n%A\n%dms\n\n" s "<null>" t

[<EntryPoint>]
let main argv =
    if argv.Length >=1 then
        match argv.[0] with
        | dir when Directory.Exists(argv.[0]) ->
            for f in Directory.EnumerateFiles(dir) do
                test (File.ReadAllText f)
        | file ->
            test (File.ReadAllText file)
    // test "foo(x,y=77) = 90"
    // test "foo(x,y=77) = 90"
    // test "foo(x,y=77) = x * y + sin(x * cos(y + 0.4))"
    0