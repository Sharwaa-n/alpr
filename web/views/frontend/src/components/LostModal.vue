<template>
<div>
    <!-- Button trigger modal -->
    <button type="button" class="btn btn-primary btn-sm" data-toggle="modal" data-target="#exampleModal">
        <slot>Add Lost Claim</slot>
    </button>


    <!-- Modal -->
    <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
        <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">Lost Claim</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
            </button>
        </div>
        <form @submit.prevent.stop="save">
            <div class="modal-body">
            <div class="form-group">
                <label for="recipient-name" class="col-form-label">License Plate:</label>
                <input type="text" v-model="data.plate" required class="form-control" id="recipient-name">
            </div>
            <div class="form-group">
                <label for="message-text" class="col-form-label">Details:</label>
                <textarea class="form-control" required v-model="data.remarks"  id="message-text"></textarea>
            </div>
            </div>
            <div class="modal-footer">
                <button type="button" :disabled='saving' class="btn btn-secondary" data-dismiss="modal">Close</button>
                <button type="submit" :disabled='saving' class="btn btn-primary">Save changes</button>
            </div>
        </form>
        </div>
    </div>
    </div>
</div>
</template>

<script>
export default {

    props: ['model'],
    data() {
        return {
            saving: false,
            data: {
                plate: null,
                remarks: null,
                ...this.model
            }
        }
    },
    methods: {
        save(){
            this.saving = true
            this.$api.post('http://localhost:5000/api/lost/', this.data).then(a => a.data).then(a => {
                this.$emit('saved', a);
                this.data = {}
                window.jQuery('#exampleModal').modal('hide')
            }).catch(err => {
                console.log(err);
            }).finally(() => this.saving = false)
            // setTimeout(() => this.saving = false ,2000)
        }
    }


}
</script>

<style>

</style>