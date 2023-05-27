
<template>
    <div class="p-2">
      <table>

        
        <thead>
          <tr
            v-for="headerGroup in table.getHeaderGroups()"
            :key="headerGroup.id"
          >


            <th
              v-for="header in headerGroup.headers"
              :key="header.id"
              :colSpan="header.colSpan"
            >
              <FlexRender
                v-if="!header.isPlaceholder"
                :render="header.column.columnDef.header"
                :props="header.getContext()"
              />
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in table.getRowModel().rows" :key="row.id">
            <td v-for="cell in row.getVisibleCells()" :key="cell.id">
              <FlexRender
                :render="cell.column.columnDef.cell"
                :props="cell.getContext()"
              />
            </td>
          </tr>
        </tbody>

      </table>
      <div class="h-4" />
      <button @click="rerender" class="border p-2">Rerender</button>
    </div>
  </template>
  
  
  <script setup lang="ts">
import {
  FlexRender,
  getCoreRowModel,
  useVueTable,
  createColumnHelper,
} from '@tanstack/vue-table'
import { ref } from 'vue'

type Person = {
  firstName: string
  lastName: string
  age: number
  visits: number
  status: string
  progress: number
}

const defaultData: Person[] = [
  {
    firstName: 'tannerxxxxxxxxxxxxxx',
    lastName: 'linsley',
    age: 24,
    visits: 100,
    status: 'In Relationship',
    progress: 50,
  },
  {
    firstName: 'tandy',
    lastName: 'miller',
    age: 40,
    visits: 40,
    status: 'Single',
    progress: 80,
  },
  {
    firstName: 'joe',
    lastName: 'dirte',
    age: 45,
    visits: 20,
    status: 'Complicated',
    progress: 10,
  },
]

const columnHelper = createColumnHelper<Person>()

const columns = [
  columnHelper.group({
    header: ' ',
    columns: [
      columnHelper.accessor('firstName', {
        cell: info => info.getValue(),
      }),
      columnHelper.accessor(row => row.lastName, {
        id: 'lastName',
        cell: info => info.getValue(),
        header: () => 'Last Name',
      }),
      columnHelper.accessor(row => row.age, {
        id: 'age',
        cell: info => info.getValue(),
        header: () => 'Age',
      }),
      columnHelper.accessor(row => row.visits, {
        id: 'visits',
        cell: info => info.getValue(),
        header: () => 'Last Name',
      }),
      columnHelper.accessor(row => row.lastName, {
        id: 'lastName',
        cell: info => info.getValue(),
        header: () => 'Last Name',
      }),
    ],
  }),
]

const data = ref(defaultData)

const rerender = () => {
  data.value = defaultData
}

const table = useVueTable({
  get data() {
    return data.value
  },
  columns,
  getCoreRowModel: getCoreRowModel(),
})
</script>



<style>

table {
  border: 1px solid lightgray;
  width:100%
}

tbody {
  border-bottom: 1px solid lightgray;
}

th {
  border-bottom: 1px solid lightgray;
  border-right: 1px solid lightgray;
  padding: 2px 4px;
  color:#fff
}

tfoot {
  color: gray;
}

tfoot th {
  font-weight: normal;
}

td{
    color:#fff
}
</style>
