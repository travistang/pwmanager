<template>
    <div>
        <div class="hidden">
          <input type="text" :id="password.name" :value="password.password" />
        </div>
        <mu-list-item class="list-item" :title="password.name" @click="copyToClipboard">
          <mu-avatar :icon="iconTag" slot="leftAvatar"/>
          <span slot="describe"> {{description}}</span>
          <mu-icon-menu icon="more_horiz" slot="right" tooltip="Action" @click.stop>
              <mu-menu-item title="Edit" @click="editPassword"/>
              <mu-menu-item title="Delete" @click="deletePassword"/>
          </mu-icon-menu>

        </mu-list-item>
    </div>
</template>

<script>
import _ from 'lodash'

export default {
  name: 'password-item',
  props: ['password'],
  data () {
    return {
    }
  },

  computed: {
    iconTag: {
      get () {
        return _.toUpper(this.password.name[0])
      }
    },
    description:{
      get() {
        // TODO: me
        const createdDate = this.getDateStringFromDate(this.password.createdAt)
        const updatedDate = this.getDateStringFromDate(this.password.updatedAt)
          let        desc = "Created at: " + createdDate
        if (createdDate != updatedDate)
        {
            desc = `${desc}\n Updated at: ${updatedDate}`
        }
        return desc;
      }
    }
  },
  methods: {
    copyToClipboard: function()
    {
      document.getElementById(this.password.name).focus();
      document.execCommand('selectAll');
      document.execCommand('copy');
      this.$emit("passwordClicked");
    },
    getDateStringFromDate: function(dateStr)
    {
      return new Date(dateStr).toISOString().slice(0,10)
    },
    deletePassword: function()
    {
      this.$emit('deletePassword',this.password)
    },
    editPassword: function()
    {
      // TODO: this
    },
  }
}
</script>
<style scoped>
.hidden{
  width: 0;
  height:0;
  opacity: 0%;
  position: relative;
}
</style>
