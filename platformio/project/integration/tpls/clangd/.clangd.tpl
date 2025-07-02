% from platformio.compat import shlex_join
%
# PlatformIO generated .clangd configuration
# This file provides clangd with the correct include paths and compiler flags
# for your PlatformIO project.

CompileFlags:
  # Use compilation database for all compiler flags and include paths
  CompilationDatabase: .
  
  # Additional flags for ESP32/Xtensa compatibility
  Add:
    # Language standards
    - -std=gnu99
    - -std=gnu++11
    # ESP32/Xtensa specific definitions
    - -D__XTENSA__
    - -D__STDC_WANT_LIB_EXT1__=1
    - -D__STDC_NO_VLA__=1
    - -D__STDC_NO_COMPLEX__=1
    - -D__USE_GNU
    - -D_GNU_SOURCE
    # Include paths (fallback if not in compile_commands.json)
% for include in filter_includes(includes):
    - -I{{ !include }}
% end
    # Preprocessor definitions (fallback if not in compile_commands.json)
% for define in defines:
    - -D{{ !define }}
% end
    # C++ standard (if specified)
% if 'cxx_stds' in locals() and cxx_stds:
    - -std={{ cxx_stds[-1] }}
% end
    # C standard (if specified)
% if 'cc_stds' in locals() and cc_stds:
    - -std={{ cc_stds[-1] }}
% end

# Index settings
Index:
  Background: Build

# Inlay hints
InlayHints:
  Enabled: Yes
  ParameterNames: Yes
  DeducedTypes: Yes
  Designators: Yes
  BlockLevel: Yes
  FunctionLikeReturnTypes: Yes
  VariableTypes: Yes

# Diagnostics
Diagnostics:
  ClangTidy:
    Add: [modernize*, performance*, readability*]
    Remove: [modernize-use-trailing-return-type]

# Formatting
Format:
  BasedOnStyle: LLVM
  IndentWidth: 2
  TabWidth: 2
  UseTab: Never
  AccessModifierOffset: -2
  AlignAfterOpenBracket: Align
  AlignConsecutiveAssignments: false
  AlignConsecutiveDeclarations: false
  AlignEscapedNewlines: Left
  AlignOperands: true
  AlignTrailingComments: true
  AllowAllParametersOfDeclarationOnNextLine: true
  AllowShortBlocksOnASingleLine: false
  AllowShortCaseLabelsOnASingleLine: false
  AllowShortFunctionsOnASingleLine: Empty
  AllowShortIfStatementsOnASingleLine: false
  AllowShortLoopsOnASingleLine: false
  AlwaysBreakAfterReturnType: None
  AlwaysBreakBeforeMultilineStrings: true
  AlwaysBreakTemplateDeclarations: Yes
  BinPackArguments: true
  BinPackParameters: true
  BraceWrapping:
    AfterClass: false
    AfterControlStatement: false
    AfterEnum: false
    AfterFunction: false
    AfterNamespace: false
    AfterStruct: false
    AfterUnion: false
    BeforeCatch: false
    BeforeElse: false
    IndentBraces: false
  BreakBeforeBinaryOperators: None
  BreakBeforeBraces: Attach
  BreakBeforeTernaryOperators: true
  BreakStringLiterals: true
  ColumnLimit: 100
  CommentPragmas: '^ IWYU pragma:'
  ConstructorInitializerAllOnOneLineOrOnePerLine: true
  ConstructorInitializerIndentWidth: 4
  ContinuationIndentWidth: 4
  Cpp11BracedListStyle: true
  DerivePointerAlignment: false
  DisableFormat: false
  ExperimentalAutoDetectBinPacking: false
  FixNamespaceComments: true
  IncludeBlocks: Preserve
  IndentCaseLabels: true
  IndentPPDirectives: None
  IndentWrappedFunctionNames: false
  KeepEmptyLinesAtTheStartOfBlocks: false
  MaxEmptyLinesToKeep: 1
  NamespaceIndentation: None
  PenaltyBreakBeforeFirstCallParameter: 1
  PenaltyBreakComment: 300
  PenaltyBreakFirstLessLess: 120
  PenaltyBreakString: 1000
  PenaltyExcessCharacter: 1000000
  PenaltyReturnTypeOnItsOwnLine: 200
  PointerAlignment: Left
  RawStringFormats:
    - Language: Cpp
      Delimiters:
        - cc
        - CC
        - cpp
        - Cpp
        - CPP
      BasedOnStyle: google
  ReflowComments: true
  SortIncludes: true
  SortUsingDeclarations: true
  SpaceAfterCStyleCast: false
  SpaceAfterTemplateKeyword: true
  SpaceBeforeAssignmentOperators: true
  SpaceInEmptyParentheses: false
  SpacesBeforeTrailingComments: 1
  SpacesInAngles: false
  SpacesInContainerLiterals: false
  SpacesInCStyleCastParentheses: false
  SpacesInParentheses: false
  SpacesInSquareBrackets: false
  Standard: Auto 