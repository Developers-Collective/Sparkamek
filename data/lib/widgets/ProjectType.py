#----------------------------------------------------------------------

    # Libraries
from .project import *
from .ProjectKeys import ProjectKeys
#----------------------------------------------------------------------

    # Class
class ProjectType:
    def __new__(cls) -> None:
        return None

    @staticmethod
    def get_all() -> list[type[SubProjectWidgetBase]]:
        return [
            LoaderWidget,
            KamekWidget,
            ReggieNextWidget,
            RiivolutionWidget,
        ]

    @staticmethod
    def get_all_keys() -> list[ProjectKeys]:
        return [project.type for project in ProjectType.get_all()]

    @staticmethod
    def get_by_type(type: ProjectKeys) -> type[SubProjectWidgetBase] | None:
        for project in ProjectType.get_all():
            if project.type == type:
                return project
        return None
#----------------------------------------------------------------------
