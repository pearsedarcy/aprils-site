from wagtail.blocks import (
    CharBlock,
    StructBlock,
    ListBlock,
    RichTextBlock,
    DateBlock,
    StreamBlock,
)
from wagtail.documents.blocks import DocumentChooserBlock
from base.blocks import BaseStreamBlock

class CVDocumentBlock(StructBlock):
    """A block for the CV document upload and display."""
    document = DocumentChooserBlock(
        required=True,
        help_text="Upload your CV document (PDF recommended)"
    )

    class Meta:
        icon = "doc-full"
        template = "cv/blocks/cv_document_block.html"

class ExperienceBlock(StructBlock):
    """A block for work experience entries."""
    company = CharBlock(help_text="Company or organization name")
    position = CharBlock(help_text="Your job title")
    date_from = DateBlock()
    date_to = DateBlock(required=False, help_text="Leave blank if this is your current position")
    description = RichTextBlock(
        features=["bold", "italic", "link"],
        help_text="Describe your responsibilities and achievements"
    )

    class Meta:
        icon = "date"
        template = "cv/blocks/experience_block.html"

class EducationBlock(StructBlock):
    """A block for education entries."""
    institution = CharBlock()
    degree = CharBlock()
    date_from = DateBlock()
    date_to = DateBlock(required=False)
    description = RichTextBlock(
        features=["bold", "italic", "link"],
        required=False
    )

    class Meta:
        icon = "education"
        template = "cv/blocks/education_block.html"

class SkillsBlock(StructBlock):
    """A block for grouping related skills."""
    category = CharBlock(help_text="Skill category (e.g., 'Programming Languages')")
    skills = ListBlock(
        CharBlock(),
        help_text="Add individual skills in this category"
    )

    class Meta:
        icon = "skills"
        template = "cv/blocks/skills_block.html"

class CVStreamBlock(BaseStreamBlock):
    """StreamBlock for building CV pages."""
    cv_document = CVDocumentBlock(group="Content")
    experience = ExperienceBlock(group="Content")
    education = EducationBlock(group="Content")
    skills = SkillsBlock(group="Content")
