export interface Tag {
  id: number
  name: string
  category: string
}

export interface Resume {
  id: number
  candidate_name: string
  file_url: string
  file_type: string
  ocr_content: string
  parsed_content: string
  talent_portrait: string
  tags: Tag[]
  created_at: string
  updated_at: string
}
