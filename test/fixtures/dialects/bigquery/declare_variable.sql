declare var1 int64;
declare var2, var3 string;
declare var4 default 'value';
declare var5 int64 default 1 + 2;
declare arr1 array<string>;
declare arr2 default ['one', 'two'];
declare arr3 default [];
declare arr4 array<string> default ['one', 'two'];
declare str1 struct<f1 string, f2 string>;
declare str2 struct<f1 string, f2 string> default struct('one', 'two');
declare str3 default struct('one', 'two');
declare str4 struct<f1 string, f2 string> default ('one', 'two');
