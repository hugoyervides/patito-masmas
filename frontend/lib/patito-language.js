// Patito ++ language definition for the Monaco editor: Monarch tokenizer,
// language configuration, completions/snippets and the editor theme.

export const KEYWORDS = [
  'programa', 'principal', 'var', 'funcion', 'return', 'void',
  'lee', 'escribe', 'si', 'entonces', 'sino', 'mientras', 'haz',
  'desde', 'hasta', 'hacer', 'null',
];

export const TYPE_KEYWORDS = ['int', 'float', 'char'];

export const DEFAULT_CODE = `programa hola;

principal(){
\t%% Mi primer programa en Patito ++
\tescribe("Hola, mundo!");
}
`;

export function registerPatitoLanguage(monaco) {
  if (monaco.languages.getLanguages().some((lang) => lang.id === 'patito')) {
    return;
  }

  monaco.languages.register({ id: 'patito' });

  monaco.languages.setMonarchTokensProvider('patito', {
    keywords: KEYWORDS,
    typeKeywords: TYPE_KEYWORDS,
    tokenizer: {
      root: [
        [/%%.*$/, 'comment'],
        [/[a-zA-Z][a-zA-Z0-9]*/, {
          cases: {
            '@keywords': 'keyword',
            '@typeKeywords': 'type',
            '@default': 'identifier',
          },
        }],
        [/\d+\.\d+/, 'number.float'],
        [/\d+/, 'number'],
        [/"[^"]*"/, 'string'],
        [/'[A-Za-z]'/, 'string'],
        [/[{}()[\]]/, '@brackets'],
        [/(&&|\|\||==|!=|>=|<=)/, 'operator'],
        // Unary matrix operators: determinant ($), transpose (¡), inverse (?)
        [/[$¡?]/, 'keyword.matrix'],
        [/[<>=+\-*/]/, 'operator'],
        [/[;,.:]/, 'delimiter'],
      ],
    },
  });

  monaco.languages.setLanguageConfiguration('patito', {
    comments: { lineComment: '%%' },
    brackets: [['{', '}'], ['[', ']'], ['(', ')']],
    autoClosingPairs: [
      { open: '{', close: '}' },
      { open: '[', close: ']' },
      { open: '(', close: ')' },
      { open: '"', close: '"' },
      { open: "'", close: "'" },
    ],
  });

  monaco.languages.registerCompletionItemProvider('patito', {
    provideCompletionItems(model, position) {
      const word = model.getWordUntilPosition(position);
      const range = {
        startLineNumber: position.lineNumber,
        endLineNumber: position.lineNumber,
        startColumn: word.startColumn,
        endColumn: word.endColumn,
      };
      const keywordItems = KEYWORDS.concat(TYPE_KEYWORDS).map((keyword) => ({
        label: keyword,
        kind: monaco.languages.CompletionItemKind.Keyword,
        insertText: keyword,
        range,
      }));
      const snippetRule = monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet;
      const snippets = [
        {
          label: 'programa',
          kind: monaco.languages.CompletionItemKind.Snippet,
          insertText: 'programa ${1:nombre};\n\nprincipal(){\n\t$0\n}\n',
          insertTextRules: snippetRule,
          documentation: 'Estructura basica de un programa',
          range,
        },
        {
          label: 'si-sino',
          kind: monaco.languages.CompletionItemKind.Snippet,
          insertText: 'si(${1:condicion}) entonces{\n\t$2\n}sino{\n\t$0\n}',
          insertTextRules: snippetRule,
          documentation: 'Condicional si / sino',
          range,
        },
        {
          label: 'mientras',
          kind: monaco.languages.CompletionItemKind.Snippet,
          insertText: 'mientras(${1:condicion}) haz{\n\t$0\n}',
          insertTextRules: snippetRule,
          documentation: 'Ciclo mientras',
          range,
        },
        {
          label: 'desde',
          kind: monaco.languages.CompletionItemKind.Snippet,
          insertText: 'desde ${1:i} = ${2:0} hasta ${3:10} hacer{\n\t$0\n}',
          insertTextRules: snippetRule,
          documentation: 'Ciclo desde / hasta',
          range,
        },
        {
          label: 'funcion',
          kind: monaco.languages.CompletionItemKind.Snippet,
          insertText: 'funcion ${1:int} ${2:nombre}(${3:int parametro}){\n\t$0\n}',
          insertTextRules: snippetRule,
          documentation: 'Declaracion de funcion',
          range,
        },
      ];
      return { suggestions: keywordItems.concat(snippets) };
    },
  });

  monaco.editor.defineTheme('patito-dark', {
    base: 'vs-dark',
    inherit: true,
    rules: [
      { token: 'keyword', foreground: 'c586c0' },
      { token: 'type', foreground: '4ec9b0' },
      { token: 'keyword.matrix', foreground: 'dcdcaa', fontStyle: 'bold' },
      { token: 'comment', foreground: '6a9955' },
      { token: 'string', foreground: 'ce9178' },
      { token: 'number', foreground: 'b5cea8' },
    ],
    colors: { 'editor.background': '#1b1e26' },
  });
}
