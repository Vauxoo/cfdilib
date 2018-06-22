=======
History
=======

0.7.3
-----

- Fixed #90

0.7.2
-----

- Welcome Impuesto Locales.
- Proper version of click.
- Fix SAT references.

0.7.0
-----

- l10n_mx_reports: fix error in general ledger report (#78)
- [IMP] cfdilib: xsd added to generate payment complement (#75)
- Changed path to allow have xsd that are imported by others xsd in the same library, and not call to SAT page each time that is generated a new XML.
- Add catPagos.xsd file
- [FIX] cfdilib: fix xsd file name to avoid error I/O warning : failed to load external entity "tdCFDI.xsd"
- [FIX] cfdilib: changing complement node task#22554 (#76)
- [FIX] l10n_mx_reports: fix error in general ledger report (#81) when "Concepto" has a length over 300 characters in operations and over 200 characters in transactions. And, when account description has a length over 100 characters.
- [FIX][cfdilib] - Welcome template for comercio exterior node.

0.6.4
-----

In some cases the RFC is optional

0.6.3
-----

Now certificate is optional on CFDI 3.3

0.6.2
-----

Add new XSD version for CFDI 3.3

0.6.1
-----

Added complement for Paymens

0.6.0
-----

- Welcome to electronic accounting 1.3

0.5.3
-----

- Added Payroll 1.2
- Added pedimento concept for cfdi 3.3.

0.5.2
-----

- Some values are now optionals.


0.5.1
-----

Some fixes regarding the fact that perceptions and taxes are optionals.

0.5.0
-----

Welcome to cfdi 3.3

0.4.0
-----

Welcome to payroll generation

0.3.5
-----

Now the template 3.2 has a placeholder for addenda.

0.3.4
-----

* XMl for Journal Items: Assigned id by the next:

Atributo requerido para expresar el número único de identificación de la
póliza. El campo deberá contener la clave o nombre utilizado por el
contribuyente para diferenciar, el tipo de póliza y el número correspondiente.
En un mes ordinario no debe repetirse un mismo número de póliza con la clave o
nombre asignado por el contribuyente.

0.3.3
-----

* Refactor of the code for cache the temp downloaded files.
* Fixed minor lint problems to improve the readability of the code.

latest
------

* Refactor of the code for cache the temp downloaded files.
* Fixed minor lint problems to improve the readability of the code.

0.3.1
-----

* Refactiring the validation approach to use a proper way and not be sticked to
  an specific lxml version

0.3.0
------

* Electronic accounting ready.

  * CoA.
  * Moves.
  * Balance


0.1.0 (2016-1-22)
------------------

* First release on PyPI.
