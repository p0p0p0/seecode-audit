# coding: utf-8


class CodeBaseException(Exception):
    pass


class SeeCodeMissingImportantParameters(CodeBaseException):
    pass


class ScanTemplateNotFound(CodeBaseException):
    pass


class SystemCommandNotFound(CodeBaseException):
    pass


class ParameterIsEmptyException(CodeBaseException):
    pass


class TaskIdIsNoneException(CodeBaseException):
    pass


class ScanTaskAlreadyExists(CodeBaseException):
    pass


class ApplicationNotFound(CodeBaseException):
    pass


class QueryConditionIsEmptyException(CodeBaseException):
    pass


class NotFoundBranchException(CodeBaseException):
    pass


class TaskConfCreateException(CodeBaseException):
    pass


class TaskProfileDisableException(CodeBaseException):
    pass


class ScanFailedException(CodeBaseException):
    pass


class FileLimitSizeException(CodeBaseException):
    pass


class SonarScannerFailureException(CodeBaseException):
    pass


class SonarScannerNotFoundException(CodeBaseException):
    pass


class SonarScannerCreateIssueFailed(CodeBaseException):
    pass


class SonarQubeAuthenticationFailed(CodeBaseException):
    pass


class HTTPStatusCodeError(CodeBaseException):
    pass
