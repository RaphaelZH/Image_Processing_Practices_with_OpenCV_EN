#

## Flowchart for Jupyter Notebook File Compression and Status Logging

```mermaid
---
config:
    flowchart:
        subGraphTitleMargin:
            top: 12
            bottom: 4
---
flowchart TB
    classDef Terminal_Symbol fill: #e86288, stroke: #f88e97, stroke-width: 2px, color: #f5f7f6

    classDef Initialization_Symbols fill: #a04e78, stroke: #e683a9, stroke-width: 2px, color: #f5f7f6

    classDef Decision_Symbol fill: #fc776a, stroke: #ffa269, stroke-width: 2px, color: #f5f7f6

    classDef Process_Symbol fill: #e17f47, stroke: #faa12f, stroke-width: 2px, color: #f5f7f6

    classDef Predefined_Process_Symbol fill: #106972, stroke: #0088a5, stroke-width: 2px, color: #f5f7f6

    classDef Background_Subgraph fill: #747ea0, stroke: #c1d6ea, stroke-width: 4px, font-size: 16pt, color: #f5f7f6, stroke-dasharray: 12 8

    subgraph LOOP_1[The Process of Looping #1]
        LOOP_1_A(LOOP \n ENTRY):::Terminal_Symbol
        LOOP_1_B{{LOOP \n INITIALIZATION}}:::Initialization_Symbols
        LOOP_1_C{Condition \n #2}:::Decision_Symbol
        LOOP_1_D[Statement \n #2]:::Process_Symbol
        LOOP_1_E(LOOP \n EXIT):::Terminal_Symbol

        direction LR
            LOOP_1_A --> LOOP_1_B -- loop iteration --> LOOP_1_C -- True --> LOOP_1_D --> LOOP_1_B
            LOOP_1_C -- False --> LOOP_1_B -- stop iteration --> LOOP_1_E

        LOOP_1_A ~~~ LOOP_1_B ~~~ LOOP_1_C ~~~ LOOP_1_D
        LOOP_1_C ~~~ LOOP_1_E
    end

    subgraph LOOP_2[The Process of Looping #2]
        LOOP_2_A(LOOP \n ENTRY):::Terminal_Symbol
        LOOP_2_B{{LOOP \n INITIALIZATION}}:::Initialization_Symbols
        LOOP_2_C{Condition \n #3}:::Decision_Symbol
        LOOP_2_D[Statement \n #3]:::Process_Symbol
        LOOP_2_E{Condition \n #4}:::Decision_Symbol
        LOOP_2_F[Statement \n #4]:::Process_Symbol
        LOOP_2_G[Statement \n #5]:::Process_Symbol
        LOOP_2_H(LOOP \n EXIT):::Terminal_Symbol

        direction LR
            LOOP_2_A --> LOOP_2_B -- loop iteration --> LOOP_2_C -- True --> LOOP_2_D --> LOOP_2_G --> LOOP_2_B
            LOOP_2_C -- False--> LOOP_2_E -- True --> LOOP_2_F --> LOOP_2_G
            LOOP_2_E -- False --> LOOP_2_B -- stop iteration --> LOOP_2_H

        LOOP_2_A ~~~ LOOP_2_B ~~~ LOOP_2_C ~~~ LOOP_2_D ~~~ LOOP_2_E ~~~ LOOP_2_F ~~~ LOOP_2_G
        LOOP_2_F ~~~ LOOP_2_H

    end

    LOOP_1:::Background_Subgraph
    LOOP_2:::Background_Subgraph

    A(START):::Terminal_Symbol
    B{Condition \n #1}:::Decision_Symbol
    C[Statement \n #1]:::Process_Symbol
    D(STOP):::Terminal_Symbol

    X[[File \n Removal]]:::Predefined_Process_Symbol

    A ==> B == True ==> LOOP_1 ==> LOOP_2 ==> D
    B == False ==> C ==> D
    X -.-> C
    X -.-> LOOP_1

    C ~~~ X

%% Colors used for the Terminal symbols in this flowchart:
%% - Pantone / PMS 17-1937 TPG / Hot Pink / #e86288 Hex Color Code
%% - Pantone / PMS 15-1624 TPG / Conch Shell / #f88e97 Hex Color Code

%% Colors used for the Initialization symbols in this flowchart:
%% - Pantone / PMS 18-2525 TPG / Magenta Haze / #a04e78 Hex Color Code
%% - Pantone / PMS 15-2217 TPG / Aurora Pink / #e683a9 Hex Color Code

%% Colors used for the Decision symbols in this flowchart:
%% - Pantone / PMS 16-1546 TPG / Living Coral / #fc776a Hex Color Code
%% - Pantone / PMS 15-1243 TPG / Papaya / #ffa269 Hex Color Code

%% Colors used for the Process symbols in this flowchart:
%% - Pantone / PMS 16-1350 TPG / Amberglow / #e17f47 Hex Color Code
%% - Pantone / PMS 15-1058 TPG / Radiant Yellow / #faa12f Hex Color Code

%% Colors used for the Predefined Process symbols in this flowchart:
%% - Pantone / PMS 18-4834 TPG / Deep Lake / #106972 Hex Color Code
%% - Pantone / PMS 17-4530 TPG / Barrier Reef / #0088a5 Hex Color Code

%% Colors used for the background of subgraphs in this flowchart:
%% - Pantone / PMS 17-3922 TPG / Blue Ice / #747ea0 Hex Color Code
%% - Pantone / PMS 13-4202 TPG / Ice Water / #c1d6ea Hex Color Code

%% Font color used for colored background and symbols in this flowchart:
%% - Pantone / PMS 11-0601 TPG / Bright White / #f5f7f6 Hex Color Code
```

> File Removal: Removes the hidden `.DS_Store` files, whose name is an abbreviation for _Desktop Services Store_, created by the macOS operating system to stores custom attributes of its containing folder, such as folder view options, icon positions, and other visual information.
>
> Condition #1: Check whether there exists a record for all Jupyter Notebook files in the current directory.
>
> Statement #1: If Condition 1 is False, create a record for all Jupyter Notebook files in the current directory immediately, while generating the corresponding pre-compressed copy for each file as well as compressing any copies that exceed the preset size limit, and recording relevant information about the copies.
>
> Condition #2: If Condition 1 is True, read this record and check whether there are certain entries in this record for which the corresponding Jupyter Notebook file cannot be found.
>
> Statement #2: If Condition 2 is True, delete these entries and eventually reset the index.
>
> Condition 3: Regardless of whether Condition 2 is True or False, check whether there are any Jupyter Notebook files in the current directory that do not have a corresponding entry in this record.
>
> Statement 3: If condition 3 is True, the information relating to the file will be added to the record as the most recent entry, and its corresponding indexes will be recorded separately in a list of indexes dedicated to recording altered or newly added entries.
>
> Condition 4: If condition 3 is False, check whether the actual modification date of the file is the same as the modification date recorded for the corresponding entry in the record.
>
> Statement 4: If condition 4 is True, update the modification date information and size information of the file to the corresponding entry in the record, and likewise record its corresponding index in the list of indexes dedicated to recording altered or newly added entries.
>
> Statement 5: Generates corresponding pre-compressed copies of the files corresponding to the entries in the records that correspond to all of the indexes in the list of indexes, compresses any copies that exceed the preset size limit, while recording information related to the corresponding copies.
>
> Statement 6: Sorts the updated record and resets its index.
