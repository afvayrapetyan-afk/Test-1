import { createContext, useContext, useState, ReactNode } from 'react'

interface FilterState {
  scoreMin: number
  scoreMax: number
  investmentMax: number
  isTrending: boolean | null
}

interface FilterContextType {
  filters: FilterState
  setFilters: (filters: FilterState) => void
  resetFilters: () => void
}

const defaultFilters: FilterState = {
  scoreMin: 0,
  scoreMax: 10,
  investmentMax: 1000000,
  isTrending: null,
}

const FilterContext = createContext<FilterContextType | undefined>(undefined)

export function FilterProvider({ children }: { children: ReactNode }) {
  const [filters, setFilters] = useState<FilterState>(defaultFilters)

  const resetFilters = () => {
    setFilters(defaultFilters)
  }

  return (
    <FilterContext.Provider value={{ filters, setFilters, resetFilters }}>
      {children}
    </FilterContext.Provider>
  )
}

export function useFilters() {
  const context = useContext(FilterContext)
  if (context === undefined) {
    throw new Error('useFilters must be used within a FilterProvider')
  }
  return context
}
