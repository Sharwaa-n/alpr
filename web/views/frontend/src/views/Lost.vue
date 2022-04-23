<template>
  <div>
      <div class="pb-4 d-flex justify-content-between">

        <h4 >
            Lost Registry ({{ pager.total_items || 0 }})
        </h4>

        <div class="d-flex justify-content-end align-items-center">
            <form @submit.prevent="searched" class="mb-0 pr-2">
                <input type="search" class="form-control" v-model="q" name="q" placeholder="Search">
            </form>
            <LostModal @saved=" item => this.items.unshift(item) "></LostModal>
        </div>
      </div>

    




    <div class="row">
        <div v-for='item in items' :key="item.id" class="col-md-3 p-2">
            <div class="card ">
                <div class="card-header d-flex justify-content-between">{{ item.plate.number }} <div class="badge" :class="{'badge-danger': item.state == 1, 'badge-success': item.state == 2 }" >{{ item.stateName }}</div></div>
                <div class="card-body">
                    <p>Date: {{ item.created_date && new Date(item.created_date).toISOString().substring(0, 10) }}</p>
                    <i>{{ item.remarks }}</i>
                </div>
                <div class="card-footer" v-if='item.state == 1'>
                    <button @click='updateStatus(item, 2)' class="btn btn-success btn-sm" >Mark as found</button>
                </div>
            </div>
        </div>
    </div>
    <div class="d-flex justify-content-end" v-if='pager.total_pages > 1'>
            <v-pagination @input="loadData" v-model="pager.page" :classes="bootstrapPaginationClasses" :page-count="pager.total_pages"></v-pagination>
    </div>

  </div>
</template>

<script>
import LostModal from '../components/LostModal'
import vPagination from 'vue-plain-pagination'
export default {
    components: {
        LostModal,
        vPagination,
    },
    data() {
        return {
            q: '',
            bootstrapPaginationClasses: {
                ul: 'pagination',
                li: 'page-item',
                liActive: 'active',
                liDisable: 'disabled',
                button: 'page-link'  
            },
            items: [],
            pager: {
                page: 1,
                total_pages: 1,
            },
            params: {

            }
        }
    },
    mounted(){
        this.q = this.$route.query.q
        this.pager.page = this.$route.query.page
        this.loadData()
    },
    methods: {
        updateStatus(item, state) {
            console.log('Updating item:', item,' State:', state);

            this.$api.put(`http://localhost:5000/api/lost/${item.id}`, { state }).then(resp => resp.data).then(data => {

                this.items.filter(i => i.id == data.id).forEach(e => {
                    console.log(this.items.indexOf(e));
                    this.items[this.items.indexOf(e)] = e
                    // this.$set(this.items, this.items.indexOf(e), e)
                })
                console.log();
                // this.items = data.data
                // this.pager = data.pager
            }) 
        },
        state(status) {
            const states = ['Missing', 'Found']
            return states[status] || 'Missing'
        },
        loadData() {
            this.$api.get('http://localhost:5000/api/lost/', { params: { ...this.$route.query, ...this.pager } }).then(resp => resp.data).then(data => {
                this.items = data.data
                this.pager = data.pager
            })  
        },
        searched(){
            // console.log(this.q);
            this.params.q = this.q;
            this.pager.page = 1

            console.log({params: this.params});

            this.$router.replace({
                path: this.$route.path,
                query: this.params
            })
            this.loadData()

        }
    }

}
</script>

<style>

</style>