<template>
    <v-container fluid class="pa-0 fill-height">
        <v-navigation-drawer app class="pa-6" clipped color="transparent" width="300" permanent floating>
            <v-autocomplete :items="tags" item-text="name" item-value="name" autofocus
                            label="Tags" multiple clearable v-model="filterTags" chips placeholder="Search tags"
                            color="purple">
                <template v-slot:prepend><v-icon color="purple">mdi-tag-multiple-outline</v-icon></template>
            </v-autocomplete>
        </v-navigation-drawer>
        <v-container class="align-self-start px-12 pt-12 flex-column">
            <v-hover v-for="blog in blogs" >
                <template v-slot:default="{hover}">
                    <v-card class="mx-12 mt-12" shaped outlined style="margin-bottom: 96px">
                        <v-card-title class="pa-0">
                            <v-chip label dark class="purple pa-5 mt-n6 ml-6 overline font-weight-regular"
                                    style="background:linear-gradient(60deg, #DA22FF 20%, #9733EE 80%)">
                                {{ blog.title }}
                            </v-chip>
                            <v-spacer></v-spacer>
                            <span class="mr-3 subtitle-2">
                                By <i>{{ blog.author.firstName + ' ' + blog.author.lastName }}</i>
                            </span>
                        </v-card-title>
                        <v-card-title class="d-block">
                            Updated on <i>{{ moment(blog.updatedAt).format('MMMM Do YYYY') }}</i>
                        </v-card-title>
                        <v-card-subtitle class="pb-0">
                            Published on <i>{{ moment(blog.publishedAt).format('MMMM Do YYYY') }}</i>
                        </v-card-subtitle>
                        <div style="position: relative">
                            <v-card-text v-html="blog.content" style="height: 200px;" class="overflow-hidden px-12"></v-card-text>
                            <div :style="'position:absolute;top:0;left:0;width:100%;height:100%;background:linear-gradient(transparent,' + ($vuetify.theme.dark ? '#1F1F1F' : 'white') + ');'">
                            </div>
                        </div>
                        <v-card-actions class="px-4 py-5 justify-space-around">
                            <v-chip tile v-for="tag in blog.tags" class="caption">
                                {{tag.name}}
                                <v-icon right color="purple lighten-1">mdi-tag-text-outline</v-icon>
                            </v-chip>
                        </v-card-actions>
                        <v-fade-transition>
                            <v-overlay absolute v-if="hover" opacity=".9" color="weak" class="mt-n6" z-index="4">
                                <v-btn dark large style="background:linear-gradient(60deg, #DA22FF 20%, #9733EE 80%)" tile>
                                    Read on<v-icon right>mdi-chevron-double-right</v-icon>
                                </v-btn>
                            </v-overlay>
                        </v-fade-transition>
                    </v-card>
                </template>
            </v-hover>
        </v-container>
    </v-container>
</template>
<script>
    import gql from 'graphql-tag'

    export default {
        apollo: {
            tags: gql`query { tags { name } }`,
            blogs: {
                query: gql`query ($tags: [String]!) { blogs (tags: $tags) {
                        title
                        publishedAt
                        updatedAt
                        content
                        tags { name }
                        author { firstName lastName }
                    }
                }`,
                variables() {
                    return {tags: this.filterTags}
                }
            }
        },

        data: () => ({
            filterTags: []
        })
    }
</script>

<style>
    .v-autocomplete:not(.v-input--is-focused).v-select--chips input {
        max-height: revert !important;
    }
</style>
